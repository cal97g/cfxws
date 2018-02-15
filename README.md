# CFXWS
Cryptocurrency websockets.

The aim of this library is to provide a standardised interface for retrieving websockets data from cryptocurrency exchanges.

## Exchanges

|EXCHANGE|STATUS|
|:-:|:-:|
|BINANCE|IN PROGRESS|
|BITFINEX|TODO|
|CEX|TODO|
|BITTREX|PRIV??|
|KUCOIN|PRIV??|

## Quickstart

While the project does not have a working exchange yet I envision the usage api to look something like this:

```python
def handle_trade(data):
    print("trade from {}-{}. Last price {}".format(
        data['exchange'],
        data['symbol'],
        data['price']
    ))

exchange = csfxws.Binance()

client = exchange.listen_trades(handle_trade, pairs = ['btceth', 'btcada', 'usdtbtc'])
```
## Status
This project is a work in progress. It's something I am working on but is not a massive priority for me at the moment. It is functional currently but I would not recommend using it in production. 

### Contributing
Contributions are definitely welcome. When contributing please branch this repository, make any changes you would like and then create a pull request.
The aim of this project primarily is consistency, so please try to use the internal classes consistently and keep data structures as consistent as possible.
If you want to change some core behaviour or structure please contact me first.
