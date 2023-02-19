import requests, json, pandas, numpy, nltk
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plot

def print_hi(name):
    print(f'Hi, {name}')

def getNews():
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=45a3abde3f2ed8d46084b1edd357ae28c250ca6e&kind=news'
    results = requests.get(url).json()["results"]
    for result in results:
        print(result["title"])

def getCoin():
    cg = CoinGeckoAPI()
    cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true',
                 include_24hr_change='true', include_last_updated_at='true')
    cg.get_coins_markets(vs_currency='usd', ids='bitcoin', price_change_percentage='1h')

if __name__ == '__main__':
    #getNews()
    getCoin()
