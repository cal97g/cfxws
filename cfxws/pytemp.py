from exchange import Binance
from client import WSClient
from twisted.python import log
from twisted.internet import reactor, ssl

from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import connectWS


b = Binance()

def echo_trade(data):
    print("{} {} {} {}".format(data['symbol'], data['exchange'], data['quantity'], data['price']))


factory = WebSocketClientFactory("wss://stream.binance.com:9443/stream?streams=adabtc@trade/")
factory.protocol = WSClient(
        "wss://stream.binance.com:9443/stream?streams=adabtc@trade/",
        43200,
        echo_trade,
        b._handle_response
    )
if factory.isSecure:
    contextFactory = ssl.ClientContextFactory()
else:
    contextFactory = None
connectWS(factory, contextFactory)
reactor.run()
