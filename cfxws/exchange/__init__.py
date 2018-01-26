import time
import datetime
import json
import ccxt

from abc import ABCMeta, abstractmethod
from cfxws.client import WSClient
from twisted.python import log
from twisted.internet import reactor, ssl

from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import connectWS

class Exchange(object):
    """
        Baseclass for all exchanges
    """

    def _key_map_to_standard(self, keymap, tickdict):
        new_dict = {}
        for key, value in keymap.items():
            new_dict[value] =  tickdict[key]
        return new_dict

    @abstractmethod
    def _handle_response(self):
        """
            This method should be implemented by all child classes. Its purpose
            is to convert exchange responses into something useable. Exchange
            date is wrapped in different ways.
        """
        raise NotImplementedError("Child class should implement _handle_response")

    @abstractmethod
    def listen_trades(self, action, pairs = None):
        """
            This method will listen to trade events via websockets and once an
            event is fired it will call action() with the data.

            usage:

            def echo_trade(data):
                print(data['price'], data['amount_base'], data['amount_quote'])

            cfxws.Binance.listen_trades(pairs = ['BTC_ETH'], echo_trade)

            :param pairs: list of ccxt standard pairs. Defaults to all pairs.
            :param action: function - this will be called for each trade event.
        """
        raise NotImplementedError("Child class should implement _listen_trades()")


    @abstractmethod
    def listen_ticks(self, action, pairs = None):
        """
            Just price data.

            :param pairs: list of ccxt standard pairs. Defaults to all pairs.
        """
        raise NotImplementedError("Child class should implement listen_ticks()")

class Binance(Exchange):
    """
        The base endpoint is: wss://stream.binance.com:9443
        Streams can be access either in a single raw stream or a combined stream
        Raw streams are accessed at /ws/<streamName>
        Combined streams are accessed at /stream?streams=<streamName1>/<streamName2>/<streamName3>
        Combined stream events are wrapped as follows: {"stream":"<streamName>","data":<rawPayload>}
        All symbols for streams are lowercase
        A single connection to stream.binance.com is only valid for 24 hours; expect to be disconnected at the 24 hour mark
    """


    def __init__(self):
        # In the case a user does not specify symbols, we will use all of them.
        ex = ccxt.binance({'enableRateLimit': False})
        tmp_markets = ex.loadMarkets()

        self.all_markets = [x.lower().replace('/', '')
        for x in tmp_markets.keys()]

        self.exchange = 'binance'
        self.wssuri = 'wss://stream.binance.com:9443'
        self.wssport = 9443
        self.channel_map = {
            "listen_all_tick": "!ticker@arr",
            "listen_tick": "<symbol>@ticker",
            "listen_trade": "<symbol>@trade",
            "listen_agg_trade": "<symbol>@aggTrade",
            "candle": "<symbol>@kline_<interval>"
        }

        # Renew period is 24h, let's renew every 12h.
        # I'm sure I've been dced in less than 24h.
        self.renew_period_s = 43200

    def _standard_pairs_to_exchange(expairs):
        pass

    def _standardise_object(self, type, data):
        if type == 'tick':
            keymap = {
                "E": "timestamp",
                "b": "bid",
                "a": "ask",
                "s": "symbol"
            }
            new_tick_dict = self._key_map_to_standard(keymap, data)
            new_tick_dict['datetime'] = datetime.datetime.fromtimestamp(
                new_tick_dict['timestamp'] / 1000.0
            )
            new_tick_dict['original'] = data
            new_tick_dict['exchange'] = self.exchange
            return new_tick_dict
        elif type == 'trade':
            keymap = {
                "E": "timestamp",
                "t": "trade_id",
                "p": "price",
                "q": "quantity",
                "T": "trade_time",
                "m": "market_maker",
                "s": "symbol"
            }

            new_trade_dict = Exchange._key_map_to_standard(keymap, data)
            # Create any values which are not there
            new_trade_dict['datetime'] = datetime.datetime.fromtimestamp(
                new_trade_dict['trade_time']
            )
            new_trade_dict['original'] = tradedict
            new_trade_dict['exchange'] = self.exchange
            return new_trade_dict
        else:
            raise ValueError("invalid object type")

    def _handle_response(self, response, type):
        """
            Take raw json and dictify
        """
        return self._standardise_object(type, data = json.loads(response)['data'])

    def listen_ticks(self, action, pairs = None):
        """
            Will listen to binance ticks. Pass pairs in 'btceth' format.
            If no pairs we will listen to all of them.

            Your method should take one parameter, name it whatever you like,
            but you'll get a python dict in this format:

            {
                "symbol": "btceth",
                "exchange": "binance",
                "timestamp": 123352345,
                "datetime": datetime object,
                "bid": 0.112324,
                "ask": 0.150545,
                "original": {} # Original response from exchange
            }

            I have taken the concscious decision not to include volume data
            in tick updates. This is because the tick data volume is often for
            a 24h period, which is entirely useless. If you need accurate volume
            data see the listen_trades method.

            :param action: method which will handle the tick data
            :param pairs: list or None. List of symbols to listen to.
            :return WSClient instance:
        """
        if not pairs:
            pairs = self.all_markets
        else:
            if not isinstance(pairs, list):
                raise ValueError(
                "Pairs must be list or None. Ex: \
                ['btceth'],['btceth', 'btcada']"
                )

        channels = [self.channel_map['listen_tick'].replace('<symbol>', pair)
        for pair in pairs]

        # Make channels url...
        stream_url = self.wssuri + '/stream?streams='
        for channel in channels:
            stream_url += str(channel + '/')
        stream_url[:-1]


        # If we want all lists we may as well use the all pair channel built in
        # by binance.
        if pairs is None:
            stream_url = self.wssuri + '/stream?streams=' + self.channel_map['listen_all_tick']

        # TODO: Move this to a method - DRY

        factory = WebSocketClientFactory(stream_url)

        MyWs = WSClient
        MyWs._handle_response = self._handle_response
        MyWs.handle_method = action

        factory.protocol = MyWs
        if factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None

        connectWS(factory, contextFactory)
        reactor.run()

    def listen_trades(self, action, pairs = None):
        """
            Will listen to binance trades. Use this to get the last trade price.
            Pass pairs in 'btceth' format. If no pairs we will listen to all
            of them.

            Your method should take one parameter, name it whatever you like,
            but you'll get a python dict in this format:

            {
                "symbol": "btceth",
                "exchange": "binance",
                "timestamp": 123352345,
                "datetime": datetime object,
                "trade_id": 1312443,
                "price": 0.123432,
                "quantity": 4.5034,
                "trade_time": 142342345,
                "market_maker": False,
                "original": {} # Original response from exchange
            }

            :param action: method which will handle the trade data
            :param pairs: list or None. List of symbols to listen to.
            :return WSClient instance:
        """

        if not pairs:
            pairs = self.all_markets
        else:
            if not isinstance(pairs, list):
                raise ValueError("Pairs must be list or None. Ex: ['btceth'],['btceth', 'btcada']")

        channels = [self.channel_map['listen_trade'].replace('<symbol>', pair) for pair in pairs]

        stream_url = self.wssuri + '/stream?streams='
        for channel in channels:
            stream_url += str(channel + '/')
        stream_url[:-1]

        # TODO: Move this to a method - DRY

        factory = WebSocketClientFactory(stream_url)

        MyWs = WSClient
        MyWs._handle_response = self._handle_response
        MyWs.handle_method = action

        factory.protocol = MyWs
        if factory.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None

        connectWS(factory, contextFactory)
        reactor.run()
