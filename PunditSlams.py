import tweepy
import requests
import json

import api_keys

url = ('http://newsapi.org/v2/everything?'
       'qInTitle=Slams&'
       'from=2020-07-15&'
       'sortBy=popularity&'
       'apiKey=' + api_keys.newsapi)

response = requests.get(url)

response_json = response.json()
for article in response_json["articles"]: 
    print(article["title"]) 

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_keys.twitter_auth_a, api_keys.twitter_auth_b)
auth.set_access_token(api_keys.twitter_access_a, api_keys.twitter_access_b)

# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
# Create a tweet
#api.update_status("Hello Tweepy")