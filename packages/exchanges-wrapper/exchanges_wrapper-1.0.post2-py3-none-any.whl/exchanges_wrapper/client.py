#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Union
import decimal
import math
import asyncio
import random
import logging
import time

from exchanges_wrapper.http_client import HttpClient
from exchanges_wrapper.errors import BinancePyError, RateLimitReached
from exchanges_wrapper.web_sockets import UserEventsDataStream, MarketEventsDataStream, FtxPrivateEventsDataStream
from exchanges_wrapper.definitions import OrderType
from exchanges_wrapper.events import Events
import exchanges_wrapper.ftx_parser as ftx

logger = logging.getLogger('exch_srv_logger')

STATUS_TIMEOUT = 5  # sec
BINANCE_ENDPOINT = "https://api.binance.com"
BINANCE_ENDPOINT_WS = "wss://stream.binance.com:9443"


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


class Client:
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        *,
        endpoint=BINANCE_ENDPOINT,
        user_agent=None,
        proxy=None,
        session=None,
        sub_account=None,
        endpoint_ws=BINANCE_ENDPOINT_WS,
    ):
        if api_secret + api_secret == 1:
            raise ValueError(
                "You cannot only specify a non empty api_key or an api_secret."
            )
        self.api_key = api_key
        self.api_secret = api_secret
        self.sub_account = sub_account
        self.endpoint_ws = endpoint_ws
        if 'ftx' in endpoint:
            self.exchange = 'ftx'
        else:
            self.exchange = 'binance'
        self.http = HttpClient(
            api_key, api_secret, endpoint, user_agent, proxy, session,
            exchange=self.exchange, sub_account=self.sub_account,
        )
        self.user_agent = user_agent
        self.proxy = None
        self.loaded = False
        self.symbols = {}
        self.highest_precision = None
        self.rate_limits = None
        self.market_data_streams = []
        self.user_data_stream = None

    async def load(self):
        infos = await self.fetch_exchange_info()
        if infos.get('success') or infos.get('serverTime'):
            # load available symbols
            self.highest_precision = 8
            original_symbol_infos = infos["symbols"]
            for symbol_infos in original_symbol_infos:
                symbol = symbol_infos.pop("symbol")
                precision = symbol_infos["baseAssetPrecision"]
                if precision > self.highest_precision:
                    self.highest_precision = precision
                symbol_infos["filters"] = dict(
                    map(lambda x: (x.pop("filterType"), x), symbol_infos["filters"])
                )
                self.symbols[symbol] = symbol_infos
            decimal.getcontext().prec = (
                self.highest_precision + 4
            )  # for operations and rounding
            # load rate limits
            self.rate_limits = infos["rateLimits"]
            self.loaded = True
        else:
            raise Exception("Can't get exchange info, check availability and operational status of the exchange")

    async def close(self):
        await self.http.close_session()

    @property
    def events(self):
        if not hasattr(self, "_events"):
            # noinspection PyAttributeOutsideInit
            self._events = Events()
        return self._events

    async def start_user_events_listener(self, endpoint=None):
        _endpoint = endpoint or BINANCE_ENDPOINT_WS
        if self.exchange == 'binance':
            self.user_data_stream = UserEventsDataStream(self, _endpoint, self.user_agent)
            await self.user_data_stream.start()
        else:
            self.user_data_stream = FtxPrivateEventsDataStream(self,
                                                               _endpoint,
                                                               self.user_agent,
                                                               self.exchange,
                                                               self.sub_account
                                                               )
            await self.user_data_stream.start()

    async def stop_user_events_listener(self):
        if self.user_data_stream:
            await self.user_data_stream.stop()

    async def start_market_events_listener(self):
        _events = self.events.registered_streams
        logger.debug(f"start_market_events_listener._event: {_events}")
        start_list = []
        for _exchange in _events.keys():
            if _exchange == 'binance':
                _endpoint = BINANCE_ENDPOINT_WS
                market_data_stream = MarketEventsDataStream(self, _endpoint, self.user_agent, _exchange)
                self.market_data_streams.append(market_data_stream)
                start = market_data_stream.start()
                start_list.append(start)
            else:
                _endpoint = self.endpoint_ws
                for channel in self.events.registered_streams.get(_exchange):
                    market_data_stream = MarketEventsDataStream(self, _endpoint, self.user_agent, _exchange, channel)
                    self.market_data_streams.append(market_data_stream)
                    start = market_data_stream.start()
                    start_list.append(start)
        logger.debug(f"start_market_events_listener.market_data_streams: {self.market_data_streams}")
        await asyncio.gather(*start_list, return_exceptions=False)

    async def stop_market_events_listener(self):
        stop_list = []
        for market_data_stream in self.market_data_streams:
            stop = market_data_stream.stop()
            stop_list.append(stop)
        await asyncio.gather(*stop_list, return_exceptions=False)

    def assert_symbol_exists(self, symbol):
        if self.loaded and symbol not in self.symbols:
            raise BinancePyError(f"Symbol {symbol} is not valid according to the loaded exchange infos.")

    def symbol_to_ftx(self, symbol) -> str:
        symbol_info = self.symbols.get(symbol)
        return f"{symbol_info.get('baseAsset')}/{symbol_info.get('quoteAsset')}"

    def refine_amount(self, symbol, amount: Union[str, decimal.Decimal], quote=False):
        if type(amount) is str:  # to save time for developers
            amount = decimal.Decimal(amount)
        if self.loaded:
            precision = self.symbols[symbol]["baseAssetPrecision"]
            lot_size_filter = self.symbols[symbol]["filters"]["LOT_SIZE"]
            step_size = decimal.Decimal(lot_size_filter["stepSize"])
            # noinspection PyStringFormat
            amount = (
                (f"%.{precision}f" % truncate(amount if quote else (amount - amount % step_size), precision))
                .rstrip("0")
                .rstrip(".")
            )
        return amount

    def refine_price(
        self, symbol, price: Union[str, decimal.Decimal]
    ) -> decimal.Decimal:
        if isinstance(price, str):  # to save time for developers
            price = decimal.Decimal(price)

        if self.loaded:
            precision = self.symbols[symbol]["baseAssetPrecision"]
            price_filter = self.symbols[symbol]["filters"]["PRICE_FILTER"]
            price = price - (price % decimal.Decimal(price_filter["tickSize"]))
            # noinspection PyStringFormat
            price = (
                (f"%.{precision}f" % truncate(price, precision))
                .rstrip("0")
                .rstrip(".")
            )
        return price

    def assert_symbol(self, symbol):
        if not symbol:
            raise ValueError("This query requires a symbol.")
        self.assert_symbol_exists(symbol)

    # keep support for hardcoded string but allow enums usage
    @staticmethod
    def enum_to_value(enum):
        if isinstance(enum, Enum):
            enum = enum.value
        return enum

    # GENERAL ENDPOINTS

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#test-connectivity
    async def ping(self):
        return await self.http.send_api_call("/api/v3/ping", send_api_key=False)

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#check-server-time
    async def fetch_server_time(self):
        return await self.http.send_api_call("/api/v3/time", send_api_key=False)

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#exchange-information
    async def fetch_exchange_info(self):
        binance_res = {}
        if self.exchange == 'binance':
            binance_res = await self.http.send_api_call(
                "/api/v3/exchangeInfo",
                send_api_key=False
            )
        elif self.exchange == 'ftx':
            res = await self.http.send_api_call(
                "markets",
                send_api_key=False
            )
            # Convert FTX to Binance Response
            if res and res.get('success'):
                binance_res = ftx.ftx_exchange_info(res.get('result'))
        return binance_res

    # MARKET DATA ENDPOINTS

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#order-book
    async def fetch_order_book(self, symbol, limit=100):
        self.assert_symbol(symbol)
        valid_limits = []
        if self.exchange == 'binance':
            valid_limits = [5, 10, 20, 50, 100, 500, 1000, 5000]
        elif self.exchange == 'ftx':
            valid_limits = [5, 10, 20, 50, 100]
        binance_res = {}
        if limit in valid_limits:
            if self.exchange == 'binance':
                binance_res = await self.http.send_api_call(
                    "/api/v3/depth",
                    params={"symbol": symbol, "limit": limit},
                    send_api_key=False,
                )
            elif self.exchange == 'ftx':
                params = {'depth': limit}
                res = await self.http.send_api_call(
                    f"markets/{self.symbol_to_ftx(symbol)}/orderbook",
                    send_api_key=False,
                    **params,
                )
                if res and res.get('success'):
                    binance_res = ftx.ftx_order_book(res.get('result'))
        else:
            raise ValueError(
                f"{limit} is not a valid limit. Valid limits: {valid_limits}"
            )
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#recent-trades-list
    async def fetch_recent_trades_list(self, symbol, limit=500):
        self.assert_symbol(symbol)
        if limit == 500:
            params = {"symbol": symbol}
        elif 0 < limit <= 1000:
            params = {"symbol": symbol, "limit": limit}
        else:
            raise ValueError(
                f"{limit} is not a valid limit. A valid limit should be > 0 and <= to 1000."
            )
        return await self.http.send_api_call(
            "/api/v3/trades", params=params, signed=False
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#old-trade-lookup-market_data
    async def fetch_old_trades_list(self, symbol, from_id=None, limit=500):
        self.assert_symbol(symbol)
        if limit == 500:
            params = {"symbol": symbol}
        elif 0 < limit <= 1000:
            params = {"symbol": symbol, "limit": limit}
        else:
            raise ValueError(
                f"{limit} is not a valid limit. A valid limit should be > 0 and <= to 1000."
            )
        if from_id:
            params["fromId"] = from_id
        return await self.http.send_api_call(
            "/api/v3/historicalTrades", params=params, signed=False
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list
    async def fetch_aggregate_trades_list(
        self, symbol, from_id=None, start_time=None, end_time=None, limit=500
    ):
        self.assert_symbol(symbol)
        if limit == 500:
            params = {"symbol": symbol}
        elif 0 < limit <= 1000:
            params = {"symbol": symbol, "limit": limit}
        else:
            raise ValueError(
                f"{limit} is not a valid limit. A valid limit should be > 0 and <= to 1000."
            )
        if from_id:
            params["fromId"] = from_id
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return await self.http.send_api_call(
            "/api/v3/aggTrades", params=params, signed=False
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
    async def fetch_klines(self, symbol, interval, start_time=None, end_time=None, limit=500):
        self.assert_symbol(symbol)
        interval = self.enum_to_value(interval)
        if self.exchange == 'ftx':
            interval = ftx.ftx_interval(interval)
        if not interval:
            raise ValueError("This query requires correct interval value")
        binance_res = []
        if self.exchange == 'binance':
            if limit == 500:
                params = {"symbol": symbol, "interval": interval}
            elif 0 < limit <= 1000:
                params = {"symbol": symbol, "interval": interval, "limit": limit}
            else:
                raise ValueError(
                    f"{limit} is not a valid limit. A valid limit should be > 0 and <= to 1000."
                )
            if start_time:
                params["startTime"] = start_time
            if end_time:
                params["endTime"] = end_time
            binance_res = await self.http.send_api_call(
                "/api/v3/klines", params=params, signed=False
            )
        elif self.exchange == 'ftx':
            end_time = int(time.time())
            start_time = end_time - interval * limit - 1
            params = {
                'resolution': interval,
                'start_time': start_time,
                'end_time': end_time}
            res = await self.http.send_api_call(
                f"markets/{self.symbol_to_ftx(symbol)}/candles",
                send_api_key=False,
                **params,
            )
            if res and res.get('success'):
                binance_res = ftx.ftx_klines(res.get('result'), interval)
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#current-average-price
    async def fetch_average_price(self, symbol):
        self.assert_symbol(symbol)
        return await self.http.send_api_call(
            "/api/v3/avgPrice",
            params={"symbol": symbol},
            signed=False,
            send_api_key=False,
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#24hr-ticker-price-change-statistics
    async def fetch_ticker_price_change_statistics(self, symbol=None):
        if symbol:
            self.assert_symbol_exists(symbol)
            binance_res = {}
        else:
            binance_res = []
        if self.exchange == 'binance':
            binance_res = await self.http.send_api_call(
                "/api/v3/ticker/24hr",
                params={"symbol": symbol} if symbol else {},
                signed=False,
                send_api_key=False,
            )
        elif self.exchange == 'ftx' and symbol:
            resolution = 60 * 60 * 24
            end_time = int(time.time())
            start_time = end_time - resolution
            params = {
                'resolution': resolution,
                'start_time': start_time,
                'end_time': end_time}
            res = await self.http.send_api_call(
                f"markets/{self.symbol_to_ftx(symbol)}/candles",
                send_api_key=False,
                **params,
            )
            if res and res.get('success'):
                binance_res = ftx.ftx_ticker_price_change_statistics(res.get('result'), symbol, end_time)
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#symbol-price-ticker
    async def fetch_symbol_price_ticker(self, symbol=None):
        if symbol:
            self.assert_symbol_exists(symbol)
            binance_res = {}
        else:
            binance_res = []
        if self.exchange == 'binance':
            binance_res = await self.http.send_api_call(
                "/api/v3/ticker/price",
                params={"symbol": symbol} if symbol else {},
                signed=False,
                send_api_key=False,
            )
        elif self.exchange == 'ftx':
            res = await self.http.send_api_call(
                f"markets/{self.symbol_to_ftx(symbol)}" if symbol else "markets",
                send_api_key=False,
            )
            if res and res.get('success'):
                binance_res = ftx.ftx_symbol_price_ticker(res.get('result'), symbol)
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#symbol-order-book-ticker
    async def fetch_symbol_order_book_ticker(self, symbol=None):
        if symbol:
            self.assert_symbol_exists(symbol)
        return await self.http.send_api_call(
            "/api/v3/ticker/bookTicker",
            params={"symbol": symbol} if symbol else {},
            signed=False,
            send_api_key=False,
        )

    # ACCOUNT ENDPOINTS

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#new-order--trade
    async def create_order(
        self,
        symbol,
        side,
        order_type,
        time_in_force=None,
        quantity=None,
        quote_order_quantity=None,
        price=None,
        new_client_order_id=None,
        stop_price=None,
        iceberg_quantity=None,
        response_type=None,
        receive_window=None,
        test=False,
    ):
        self.assert_symbol(symbol)
        side = self.enum_to_value(side)
        order_type = self.enum_to_value(order_type)
        if not side:
            raise ValueError("This query requires a side.")
        if not order_type:
            raise ValueError("This query requires an order_type.")

        binance_res = {}
        if self.exchange == 'binance':
            params = {"symbol": symbol, "side": side, "type": order_type}
            if time_in_force:
                params["timeInForce"] = self.enum_to_value(time_in_force)
            elif order_type in [
                OrderType.LIMIT.value,
                OrderType.STOP_LOSS_LIMIT.value,
                OrderType.TAKE_PROFIT_LIMIT.value,
            ]:
                raise ValueError("This order type requires a time_in_force.")
            if quote_order_quantity:
                params["quoteOrderQty"] = self.refine_amount(
                    symbol, quote_order_quantity, True
                )
            if quantity:
                params["quantity"] = self.refine_amount(symbol, quantity)
            elif not quote_order_quantity:
                raise ValueError(
                    "This order type requires a quantity or a quote_order_quantity."
                    if order_type == OrderType.MARKET
                    else "This order type requires a quantity."
                )
            if price:
                params["price"] = self.refine_price(symbol, price)
            elif order_type in [
                OrderType.LIMIT.value,
                OrderType.STOP_LOSS_LIMIT.value,
                OrderType.TAKE_PROFIT_LIMIT.value,
                OrderType.LIMIT_MAKER.value,
            ]:
                raise ValueError("This order type requires a price.")
            if new_client_order_id:
                params["newClientOrderId"] = new_client_order_id
            if stop_price:
                params["stopPrice"] = self.refine_price(symbol, stop_price)
            elif order_type in [
                OrderType.STOP_LOSS.value,
                OrderType.STOP_LOSS_LIMIT.value,
                OrderType.TAKE_PROFIT.value,
                OrderType.TAKE_PROFIT_LIMIT.value,
            ]:
                raise ValueError("This order type requires a stop_price.")
            if iceberg_quantity:
                params["icebergQty"] = self.refine_amount(symbol, iceberg_quantity)
            if response_type:
                params["newOrderRespType"] = response_type
            if receive_window:
                params["recvWindow"] = receive_window
            route = "/api/v3/order/test" if test else "/api/v3/order"
            binance_res = await self.http.send_api_call(route, "POST", data=params, signed=True)
        elif self.exchange == 'ftx':
            params = {
                "market": self.symbol_to_ftx(symbol),
                "side": side.lower(),
                "price": float(price),
                "type": order_type.lower(),
                "size": float(quantity),
                "clientId": None
            }
            count = 0
            res = {}
            while count < 10:
                try:
                    res = await self.http.send_api_call(
                        "orders",
                        method="POST",
                        signed=True,
                        **params,
                    )
                    break
                except RateLimitReached:
                    count += 1
                    logger.info(f"RateLimitReached for {self.symbol_to_ftx(symbol)}, count {count}, try one else")
                    await asyncio.sleep(random.uniform(0.1, 0.3) * count)
            # logger.debug(f"create_order.res: {res}")
            if res and res.get('success'):
                binance_res = ftx.ftx_order(res.get('result'), response_type=False)
                if binance_res.get('status') != 'NEW':
                    order_id = binance_res.get('orderId')
                    binance_res = await self.fetch_order(symbol, order_id, receive_window)
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#query-order-user_data
    async def fetch_order(  # lgtm [py/similar-function]
        self,
        symbol,
        order_id=None,
        origin_client_order_id=None,
        receive_window=None,
        response_type=None,
    ):
        self.assert_symbol(symbol)
        binance_res = {}
        if self.exchange == 'binance':
            params = {"symbol": symbol}
            if not order_id and not origin_client_order_id:
                raise ValueError(
                    "This query requires an order_id or an origin_client_order_id"
                )
            if order_id:
                params["orderId"] = order_id
            if origin_client_order_id:
                params["originClientOrderId"] = origin_client_order_id
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/api/v3/order",
                params=params,
                signed=True,
            )
        elif self.exchange == 'ftx':
            if not order_id:
                raise ValueError(
                    "This query requires an order_id on FTX"
                )
            res = await self.http.send_api_call(
                f"orders/{order_id}",
                signed=True,
             )
            if res and res.get('success'):
                binance_res = ftx.ftx_order(res.get('result'), response_type=response_type)
        logger.debug(f"fetch_order.res: {binance_res}")
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#cancel-order-trade
    async def cancel_order(  # lgtm [py/similar-function]
        self,
        symbol,
        order_id=None,
        origin_client_order_id=None,
        new_client_order_id=None,
        receive_window=None,
    ):
        self.assert_symbol(symbol)
        binance_res = {}
        if self.exchange == 'binance':
            params = {"symbol": symbol}
            if not order_id and not origin_client_order_id:
                raise ValueError(
                    "This query requires an order_id or an origin_client_order_id."
                )
            if order_id:
                params["orderId"] = order_id
            if origin_client_order_id:
                params["originClientOrderId"] = origin_client_order_id
            if new_client_order_id:
                params["newClientOrderId"] = origin_client_order_id
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/api/v3/order",
                "DELETE",
                params=params,
                signed=True,
            )
        elif self.exchange == 'ftx':
            if not order_id:
                raise ValueError(
                    "This query requires an order_id on FTX"
                )
            await self.http.send_api_call(
                f"orders/{order_id}",
                method="DELETE",
                signed=True,
             )
            order_cancelled = False
            timeout = STATUS_TIMEOUT
            while not order_cancelled and timeout:
                timeout -= 1
                binance_res = await self.fetch_order(symbol,
                                                     order_id,
                                                     origin_client_order_id,
                                                     receive_window,
                                                     response_type=True,
                                                     )
                order_cancelled = bool(binance_res.get('status') == 'CANCELED')
                await asyncio.sleep(1)
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#cancel-all-open-orders-on-a-symbol-trade
    async def cancel_all_orders(self, symbol, receive_window=None):
        self.assert_symbol(symbol)
        binance_res = []
        if self.exchange == 'binance':
            params = {"symbol": symbol}
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/api/v3/openOrders",
                "DELETE",
                params=params,
                signed=True,
            )
        elif self.exchange == 'ftx':
            params = {'market': self.symbol_to_ftx(symbol)}
            # Get list of open orders
            res_orders = await self.http.send_api_call(
                "orders",
                signed=True,
                **params
            )
            # Delete it
            res = await self.http.send_api_call(
                "orders",
                method="DELETE",
                signed=True,
                **params
            )
            if res and res.get('success'):
                binance_res = ftx.ftx_orders(res_orders.get('result'), response_type=True)
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#current-open-orders-user_data
    async def fetch_open_orders(self, symbol, receive_window=None):
        self.assert_symbol(symbol)
        binance_res = []
        if self.exchange == 'binance':
            params = {"symbol": symbol}
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/api/v3/openOrders",
                params=params,
                signed=True
            )
        elif self.exchange == 'ftx':
            params = {'market': self.symbol_to_ftx(symbol)}
            res = await self.http.send_api_call(
                "orders",
                signed=True,
                **params,
            )
            if res and res.get('success'):
                binance_res = ftx.ftx_orders(res.get('result'))
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#all-orders-user_data
    async def fetch_all_orders(
        self,
        symbol,
        order_id=None,
        start_time=None,
        end_time=None,
        limit=500,
        receive_window=None,
    ):
        self.assert_symbol(symbol)
        if limit == 500:
            params = {"symbol": symbol}
        elif 0 < limit <= 1000:
            params = {"symbol": symbol, "limit": limit}
        else:
            raise ValueError(
                f"{limit} is not a valid limit. A valid limit should be > 0 and <= to 1000."
            )

        if order_id:
            params["orderId"] = order_id
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if receive_window:
            params["recvWindow"] = receive_window

        return await self.http.send_api_call(
            "/api/v3/allOrders",
            params=params,
            signed=True,
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#new-oco-trade
    async def create_oco(
        self,
        symbol,
        side,
        quantity,
        price,
        stop_price,
        list_client_order_id=None,
        limit_iceberg_quantity=None,
        stop_client_order_id=None,
        stop_limit_price=None,
        stop_iceberg_quantity=None,
        stop_limit_time_in_force=None,
        response_type=None,
        receive_window=None,
    ):
        self.assert_symbol(symbol)
        side = self.enum_to_value(side)
        if not side:
            raise ValueError("This query requires a side.")
        if not quantity:
            raise ValueError("This query requires a quantity.")
        if not price:
            raise ValueError("This query requires a price.")
        if not stop_price:
            raise ValueError("This query requires a stop_price.")

        params = {
            "symbol": symbol,
            "side": side,
            "quantity": self.refine_amount(symbol, quantity),
            "price": self.refine_price(symbol, price),
            "stopPrice": self.refine_price(symbol, stop_price),
            "stopLimitPrice": self.refine_price(symbol, stop_limit_price),
        }

        if list_client_order_id:
            params["listClientOrderId"] = list_client_order_id
        if limit_iceberg_quantity:
            params["limitIcebergQty"] = self.refine_amount(
                symbol, limit_iceberg_quantity
            )
        if stop_client_order_id:
            params["stopLimitPrice"] = self.refine_price(symbol, stop_client_order_id)
        if stop_iceberg_quantity:
            params["stopIcebergQty"] = self.refine_amount(symbol, stop_iceberg_quantity)
        if stop_limit_time_in_force:
            params["stopLimitTimeInForce"] = stop_limit_time_in_force
        if response_type:
            params["newOrderRespType"] = response_type
        if receive_window:
            params["recvWindow"] = receive_window

        return await self.http.send_api_call(
            "/api/v3/order/oco", "POST", data=params, signed=True
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#query-oco-user_data
    async def fetch_oco(  # lgtm [py/similar-function]
        self,
        symbol,
        order_list_id=None,
        origin_client_order_id=None,
        receive_window=None,
    ):
        self.assert_symbol(symbol)
        params = {"symbol": symbol}
        if not order_list_id and not origin_client_order_id:
            raise ValueError(
                "This query requires an order_id or an origin_client_order_id."
            )
        if order_list_id:
            params["orderListId"] = order_list_id
        if origin_client_order_id:
            params["originClientOrderId"] = origin_client_order_id
        if receive_window:
            params["recvWindow"] = receive_window

        return await self.http.send_api_call(
            "/api/v3/orderList",
            params=params,
            signed=True,
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#cancel-oco-trade
    async def cancel_oco(  # lgtm [py/similar-function]
        self,
        symbol,
        order_list_id=None,
        list_client_order_id=None,
        new_client_order_id=None,
        receive_window=None,
    ):
        self.assert_symbol(symbol)
        params = {"symbol": symbol}
        if not order_list_id and not list_client_order_id:
            raise ValueError(
                "This query requires a order_list_id or a list_client_order_id."
            )
        if order_list_id:
            params["orderListId"] = order_list_id
        if list_client_order_id:
            params["listClientOrderId"] = list_client_order_id
        if new_client_order_id:
            params["newClientOrderId"] = new_client_order_id
        if receive_window:
            params["recvWindow"] = receive_window

        return await self.http.send_api_call(
            "/api/v3/order/oco",
            "DELETE",
            params=params,
            signed=True,
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#query-open-oco-user_data
    async def fetch_open_oco(self, receive_window=None):
        params = {}

        if receive_window:
            params["recvWindow"] = receive_window

        return await self.http.send_api_call(
            "/api/v3/openOrderList",
            params=params,
            signed=True,
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#query-all-oco-user_data
    async def fetch_all_oco(
        self,
        from_id=None,
        start_time=None,
        end_time=None,
        limit=None,
        receive_window=None,
    ):
        params = {}

        if from_id:
            params["fromId"] = from_id
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if limit:
            params["limit"] = limit
        if receive_window:
            params["recvWindow"] = receive_window

        return await self.http.send_api_call(
            "/api/v3/allOrderList",
            params=params,
            signed=True,
        )

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#account-information-user_data
    async def fetch_account_information(self, receive_window=None):
        params = {}
        binance_res = {}
        if self.exchange == 'binance':
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/api/v3/account",
                params=params,
                signed=True,
            )
        elif self.exchange == 'ftx':
            res = await self.http.send_api_call(
                "wallet/balances",
                signed=True)
            if res and res.get('success'):
                binance_res = ftx.ftx_account_information(res.get('result'))
        return binance_res

    # https://binance-docs.github.io/apidocs/spot/en/#funding-wallet-user_data
    # Not can be used for Spot Test Network, for real SPOT market only
    async def fetch_funding_wallet(self, asset=None, need_btc_valuation=None, receive_window=None):
        binance_res = []
        if self.exchange == 'binance':
            params = {}
            if asset:
                params["asset"] = asset
            if need_btc_valuation:
                params["needBtcValuation"] = "true"
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/sapi/v1/asset/get-funding-asset",
                method="POST",
                params=params,
                signed=True,
            )
        elif self.exchange == 'ftx':
            res = await self.http.send_api_call(
                "wallet/all_balances",
                signed=True,
             )
            if res and res.get('success'):
                binance_res = ftx.ftx_fetch_funding_wallet(res.get('result').get('main', []))
        return binance_res

    # https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#account-trade-list-user_data
    async def fetch_account_trade_list(
        self,
        symbol,
        start_time=None,
        end_time=None,
        from_id=None,
        limit=500,
        receive_window=None,
    ):
        self.assert_symbol(symbol)
        binance_res = []
        if self.exchange == 'binance':
            if limit == 500:
                params = {"symbol": symbol}
            elif 0 < limit <= 1000:
                params = {"symbol": symbol, "limit": limit}
            else:
                raise ValueError(
                    f"{limit} is not a valid limit. A valid limit should be > 0 and <= to 1000."
                )
            if start_time:
                params["startTime"] = start_time
            if end_time:
                params["endTime"] = end_time
            if from_id:
                params["fromId"] = from_id
            if receive_window:
                params["recvWindow"] = receive_window
            binance_res = await self.http.send_api_call(
                "/api/v3/myTrades",
                params=params,
                signed=True,
            )
        elif self.exchange == 'ftx':
            params = {'market': self.symbol_to_ftx(symbol)}
            if start_time:
                params["startTime"] = int(start_time / 1000)
            if from_id:
                params["orderId"] = from_id
            res = await self.http.send_api_call(
                "fills",
                signed=True,
                **params,
            )
            if res and res.get('success'):
                binance_res = ftx.ftx_account_trade_list(res.get('result')[-limit:])
        return binance_res
    # USER DATA STREAM ENDPOINTS

    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md#create-a-listenkey
    async def create_listen_key(self):
        return await self.http.send_api_call("/api/v3/userDataStream", "POST")

    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md#close-a-listenkey
    async def keep_alive_listen_key(self, listen_key):
        if not listen_key:
            raise ValueError("This query requires a listen_key.")
        return await self.http.send_api_call(
            "/api/v3/userDataStream", "PUT", params={"listenKey": listen_key}
        )

    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md#close-a-listenkey
    async def close_listen_key(self, listen_key):
        if not listen_key:
            raise ValueError("This query requires a listen_key.")
        return await self.http.send_api_call(
            "/api/v3/userDataStream", "DELETE", params={"listenKey": listen_key}
        )
