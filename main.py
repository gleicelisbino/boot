import requests, json
from pycoingecko import CoinGeckoAPI

def print_hi(name):
    print(f'Hi, {name}')

def getNews():
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=45a3abde3f2ed8d46084b1edd357ae28c250ca6e&kind=news'
    results = requests.get(url).json()["results"]
    for result in results:
        print(result["title"])

if __name__ == '__main__':
    getNews()
