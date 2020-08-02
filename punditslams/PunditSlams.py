import tweepy
import requests
import os
import math
from dotenv import load_dotenv

from datetime import datetime
from time import sleep

from log import *

load_dotenv()

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


# Returns the current time, truncated to 15 minute intervals
def gettime_truncated():
    curr_time = datetime.utcnow()
    minutes = math.floor(curr_time.minute / 15) * 15
    return curr_time.replace(minute=minutes, second=0, microsecond=0)


if __name__ == '__main__':
    tweety = init_tweety()

    last_time = gettime_truncated()
    log_info("First time interval: {time}", time=last_time.isoformat())

    while(True):
        curr_time = gettime_truncated()
        if last_time < curr_time:
            # there should be at least 15 minutes difference, since times are truncated
            log_info("Time interval: {t0} -> {t1}", t0=last_time.isoformat(), t1=curr_time.isoformat())
            
            # Query articles in the time interval
            start = last_time.isoformat()
            end = curr_time.isoformat()
            #slam_articles = articles('slams', start_date=start, end_date=end, api_key=os.getenv("NEWSAPI_KEY"))
            #for article in slam_articles:
            #    print(article["title"])

            # get ready for the next interval
            last_time = curr_time



        # Create a tweet
        # tweety.update_status("Hello Tweepy")
        sleep(30)  # Check every 30 seconds
