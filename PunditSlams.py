import tweepy
import requests
import os
from dotenv import load_dotenv

from datetime import date
from time import sleep

load_dotenv()

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


def init_tweety():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(
        os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"),
                          os.getenv("ACCESS_TOKEN_SECRET"))

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api


if __name__ == '__main__':
    tweety = init_tweety()

    while(True):
        today = date.today()
        slam_articles = articles('slams', start_date=today, api_key=os.getenv("NEWSAPI_KEY"))
        for article in slam_articles:
            print(article["title"])

        # Create a tweet
        # tweety.update_status("Hello Tweepy")
        sleep(30)  # Check every 30 seconds
