import tweepy
import requests
import os
import math

from datetime import datetime
from time import sleep

from auth import auth
from models import Article
from log import *

NEWSAPI_URL = 'https://newsapi.org/v2/everything'


# See 'Request Parameters' section https://newsapi.org/docs/endpoints/everything
def articles(query, *, start_date, api_key, sort_by='popularity', language='en', end_date=None):

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
            'to': end_date if end_date else date.today().isoformat(),
            'language': language,
            'sortBy': sort_by,
            'page': page_count,
            'apiKey': api_key,
        }
        response = requests.get(NEWSAPI_URL, params=params)
        response_json = response.json()

        if response_json.get('status') == 'ok':
            page_articles = response_json.get('articles')
            if (page_articles == None or len(page_articles) == 0):
                break

            articles.extend(page_articles)
            page_count = page_count + 1
        else:
            log_error("NewsAPI response: '{msg}'", msg=response_json.get('message'))
            break

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


# Returns the current time, truncated to 15 minute intervals
def gettime_truncated():
    curr_time = datetime.utcnow()
    minutes = math.floor(curr_time.minute / 15) * 15
    return curr_time.replace(minute=minutes, second=0, microsecond=0)


if __name__ == '__main__':
    app = init_app()

    last_time = gettime_truncated()
    log_info("First time interval: {time}", time=last_time.isoformat())

    while(True):
        curr_time = gettime_truncated()
        if last_time < curr_time:
            # there should be at least 15 minutes difference, since times are truncated
            log_info("Time interval: {t0} -> {t1}",
                     t0=last_time.isoformat(), t1=curr_time.isoformat())

            # Query articles in the time interval
            start = last_time.isoformat()
            end = curr_time.isoformat()
            slam_articles = articles('slams', start_date=start, end_date=end,
                                     api_key=os.getenv("NEWSAPI_KEY"))
            for article in slam_articles:
                title, url = article['title'], article['url']
                app.update_status(title + '\n' + url)
                Article.create(title=title, url=url)
                log_info("Tweet:\n{msg}", msg=title + '\n' + url)

            # get ready for the next interval
            last_time = curr_time

        # Create a tweet
        # app.update_status('test')
        sleep(30)  # Check every 30 seconds
