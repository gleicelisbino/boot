import inline as inline
import matplotlib
import numpy as np
import pandas as pd
import requests, json, pandas, numpy, nltk
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plot
from textblob import TextBlob

def print_hi(name):
    print(f'Hi, {name}')
#kind=news
def getNews():
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=45a3abde3f2ed8d46084b1edd357ae28c250ca6e&currencies=BTC'
    results = requests.get(url).json()["results"]
    title = []
    sentiment = []
    for result in results:
        title.append(result["title"])
        pola = TextBlob(result["title"])
        if pola.sentiment.polarity > 0:
            sentiment.append(1)
        elif pola.sentiment.polarity == 0:
            sentiment.append(0)
        else:
            sentiment.append(-1)

    data = pd.DataFrame(data=title, columns=['News'])
    data['sentiment'] = sentiment
    print(data)

def getCoin():
    cg = CoinGeckoAPI()
    cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true',
                 include_24hr_change='true', include_last_updated_at='true')
    cg.get_coins_markets(vs_currency='usd', ids='bitcoin', price_change_percentage='1h')

if __name__ == '__main__':
    getNews()
    #getCoin()
