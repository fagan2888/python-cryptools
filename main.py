import ccxt
import time
from forex_python.converter import CurrencyRates
from binance.client import Client
from binance.enums import *
from binance_info import *
c = CurrencyRates()
exchange = ccxt.binance()
client = Client(API_KEY, API_SECRET)


def altbtccalc(x,sign,sign2):
    ''' (float, str, str) -> float
    
    Accepts an input of 'x' amount of some cryptocurrency, and converts that
    amount to its equivalent in USD. Precondition: sign2 must be either
    'ABC/BTC' or 'ABC/ETH', where ABC is our altcoin.
    
    >>> altbtccalc(100,'NEO/BTC', 'BTC/USDT')
    13581.35
    '''
    
    a = exchange.fetch_ticker(sign)
    b = exchange.fetch_ticker(sign2) #'sign2/USDT'
    #rate = c.get_rates('USD')['CAD'] # USD to CAD rate
    rate = 1.23 # USD to CAD rate
    s1_to_s2 = float(a['info']['lastPrice']) # alt to BTC or ETH rate
    s2_to_usdt = float(b['info']['lastPrice']) # BTC or ETH to USD rate
    z = (s1_to_s2 * x) * s2_to_usdt * rate
    return round(z,2)

def altbtc(sign):
    ''' (str) -> str
    
    Accepts an input of 'sign' cryptocurrency, and returns the corresponding
    balance info in your Binance wallet, in USD.
    
    >>> altbtc('ADA')
    'current ADA account: $100.00CAD'
    '''
    
    return "current " + sign + " account: $" + str(altbtccalc(assetcheck(sign),sign + '/BTC','BTC/USDT')) + "CAD"

def assetcheck(sign):
    ''' (str) -> float
    
    Accepts an input of 'sign' cryptocurrency, and returns its current balance
    in your Binance wallet, as a float.
    
    >>> assetcheck('ADA')
    0.758
    '''

    asset_balance = client.get_asset_balance(sign)['free']
    return float(asset_balance)

def btc():
    ''' NoneType -> float
    
    Returns your current $BTC balance.
    '''
    b = exchange.fetch_ticker('BTC/USDT') #'BTC/USDT'
    #rate = c.get_rates('USD')['CAD']
    rate = 1.23
    btc_to_usdt = float(b['info']['lastPrice']) # BTC to USD rate
    fin = assetcheck('BTC') * btc_to_usdt * rate
    return round(fin,2)

def adabtccalc(x):
    ''' float -> float
    
    An example of a method which simplifies an application of altbtccalc above.
    Call this method to convert 'x' in $ADA to USD
    '''
    return altbtccalc(x,'ADA/BTC', 'BTC/USDT')

def adabtc():
    ''' NoneType -> str
    
    An example of a method which simplifies an application of altbtc above.
    Call this method to retrieve your current $ADA balance info from your Binance 
    wallet, in USD.
    '''
    return altbtc('ADA')

def getprice(sign):
    ''' str -> float
    
    Returns the last price of 'sign'
    '''
    # arguments: 'XRP/ETH', 'ETH/BTC', 'XRP/BTC'
    ticker = exchange.fetch_ticker(sign)
    return float(ticker['info']['lastPrice'])
