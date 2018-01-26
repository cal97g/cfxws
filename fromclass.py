from cfxws.exchange import Binance

b = Binance()

def echo(self, data):
    print(data)

b.listen_trades(echo, ['adabtc', 'ethbtc'])
