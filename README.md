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

Crypto websockets in 8 lines of code

```python
from cfxws.exchange import Binance

b = Binance()

def echo(self, data):
    print(data)

b.listen_trades(echo, ['adabtc', 'ethbtc'])

```
## Status
This project is a work in progress. It's something I am working on but is not a massive priority for me at the moment. It is functional currently but I would not recommend using it in production. 

### Contributing
Contributions are definitely welcome. When contributing please branch this repository, make any changes you would like and then create a pull request.
The aim of this project primarily is consistency, so please try to use the internal classes consistently and keep data structures as consistent as possible.
If you want to change some core behaviour or structure please contact me first.
