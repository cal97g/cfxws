
class Exchange(object):

    self.exchange_to_standard_pair = {
        "BCC": "BCC"
        "BTX": "BTC"
    }

    @classmethod
    def standardise_pairs():
        """
            This should standardise pairs to the cfxws standard of BASE_QUOTE.
        """
        pass

    @classmethod
    def listen_trades(self, pairs = None):
        """
            :param pairs: list of ccxt standard pairs. Defaults to all pairs.
        """
        pass

    @classmethod
    def listen_ticks(self, pairs = None):
        """
            :param pairs: list of ccxt standard pairs. Defaults to all pairs.
        """
        pass

    @classmethod
    def live_orderbook(self, pair):
        """
            Live orderbook implementation in python. Use websocket information
            to build the orderbook at the current moment in time.
        """
