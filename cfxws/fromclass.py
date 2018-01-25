from exchange import Binance

b = Binance()

def echo(self, data):
    print(data)

b.listen_ticks(echo, ['adabtc', 'ethbtc'])
