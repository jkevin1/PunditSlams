import tweepy
import requests
import os

from datetime import date
from time import sleep

from auth import auth
from models import Article

NEWSAPI_URL = 'https://newsapi.org/v2/everything'


# See 'Request Parameters' section https://newsapi.org/docs/endpoints/everything
def articles(query, *, start_date, api_key, sort_by='popularity', language='en'):

    articles = []
    page_count = 1

    # Loops are for chads and jocks
    while True:
        # Some useful parameters:
        # - q: content query,
        # - domains: comma-separated domains
        # - excludeDomains:
        # - to: end date
        # - pageSize: defaults to 20, maximum is 100
        params = {
            'qInTitle': query,
            'from': start_date,
            'language': language,
            'sortBy': sort_by,
            'page': page_count,
            'apiKey': api_key,
        }
        response = requests.get(NEWSAPI_URL, params=params)
        response_json = response.json()

        # TODO branch based on 'status' field of response
        page_articles = response_json.get('articles')
        if (page_articles == None or len(page_articles) == 0):
            break

        articles.extend(page_articles)
        page_count = page_count + 1

    return articles


def init_app():
    # Create API object
    app = tweepy.API(auth)

    try:
        app.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return app


if __name__ == '__main__':
    app = init_app()

    while(True):
        today = date.today()
        slam_articles = articles('slams', start_date=today, api_key=os.getenv("NEWSAPI_KEY"))
        for article in slam_articles:
            title, url = article['title'], article['url']
            Article.create(title=title, url=url)

        # Create a tweet
        # app.update_status('test')
        sleep(30)  # Check every 30 seconds
