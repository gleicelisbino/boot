import requests, json

def print_hi(name):
    print(f'Hi, {name}')

def getNews():
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=45a3abde3f2ed8d46084b1edd357ae28c250ca6e&kind=news'
    news = requests.get(url)
    data = news.json()
    results = data["results"]
    for result in results:
        print(result["title"])

if __name__ == '__main__':
    getNews()
