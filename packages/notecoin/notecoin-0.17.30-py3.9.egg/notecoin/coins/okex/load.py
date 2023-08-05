import ccxt
from notecoin.coins.base.load import LoadDataKline

exchan = LoadDataKline(ccxt.okex())
# exchan.load('BTC/USDT')
# exchan.load('BTC/USDT')
exchan.load_all()
