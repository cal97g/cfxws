import sys
import json

from twisted.python import log
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory

log.startLogging(sys.stdout)

class WSClient(WebSocketClientProtocol):
    """
        This will handle websocket implementation.
    """
    """
    def __init__(self, wss_url, renew_period, handle_method, _handle_data):
        self.wss_url = wss_url
        self.renew_period = renew_period
        self.handle_method = handle_method
        self._handle_data = _handle_data
        print (wss_url, renew_period, handle_method, _handle_data
    """
    def _event(self, data):
        """
            This method will be the method we call to handle events. Will be async.
        """
        data = self._handle_data(data)
        handle_method(data)

    def onOpen(self):
        pass
    def _handle_data(self, response):
        return json.loads(response)['data']
    def handle_method(self, data):
        print(data)
        #print("{} {} {} {}".format(data['symbol'], data['exchange'], data['quantity'], data['price']))

    def onMessage(self, payload, isBinary):
        if isBinary:
            raise AttributeError('Must not be binary. Binary sucks.')
        else:
            self.handle_method(self._handle_data(payload.decode('utf8')))

    def _create_ws_factory(self):
        """
        factory = WebSocketClientFactory()
        factory.protocol = MyClientProtocol

        reactor.connectTCP("127.0.0.1", 9000, factory)
        """
