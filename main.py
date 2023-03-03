import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
from GoogleNews import GoogleNews

start = datetime.now() - timedelta(days=7)
end = datetime.now()
def getNews():
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=45a3abde3f2ed8d46084b1edd357ae28c250ca6e&currencies=BTC&filter=rising'
    results = requests.get(url).json()["results"]
    title = []
    sentiment = []
    for result in results:
        title.append(result["title"])
        text_blob_title = TextBlob(result["title"])
        if text_blob_title.sentiment.polarity > 0:
            sentiment.append(1)
        elif text_blob_title.sentiment.polarity == 0:
            text_blob_tags = text_blob_title.tags
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
