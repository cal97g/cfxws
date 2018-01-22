

class CfxwsWSClient(Object):
    """
        This will handle websocket implementation.
        Probably some form of async shit going on here. Who knows.
    """

    def __init__(self, wss_url, renew_period, handle_method, _handle_data):
        pass

    def _event(self, data):
        """
            This method will be the method we call to handle events. Will be async.
        """
        data = self._handle_data(data)
        handle_method(data)
