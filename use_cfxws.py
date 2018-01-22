import asyncio
import csfxws

async def handle_trade(data):
    print("trade from {}-{}. Last price {}".format(
        data['exchange'],
        data['symbol'],
        data['price']
    ))

exchange = csfxws.Binance()

client = exchange.listen_trades(handle_trade, pairs = ['btceth', 'btcada', 'usdtbtc'])

while True:
    client
