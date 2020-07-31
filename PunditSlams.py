import tweepy
import requests

import api_keys

NEWSAPI_URL = 'https://newsapi.org/v2/everything'


def articles(query, *, start_date, api_key, sort_by='popularity'):
    params = {
        'qInTitle': query,
        'from': start_date,
        'sortBy': sort_by,
        'apiKey': api_key
    }
    response = requests.get(NEWSAPI_URL, params=params)
    response_json = response.json()
    return response_json.get('articles')


def init_tweety():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_keys.twitter["CONSUMER_KEY"], api_keys.twitter["CONSUMER_KEY"])
    auth.set_access_token(api_keys.twitter["CONSUMER_KEY"], api_keys.twitter["CONSUMER_KEY"])

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api


if __name__ == '__main__':
    slam_articles = articles('slams', start_date='2020-07-28', api_key=api_keys.newsapi["KEY"])
    for article in slam_articles:
        print(article["title"])

    tweety = init_tweety()
    # Create a tweet
    #tweety.update_status("Hello Tweepy")
