import tweepy
import requests
import json

url = ('http://newsapi.org/v2/everything?'
       'q=slams&'
       'from=2020-07-28&'
       'sortBy=popularity&'
       'apiKey=<key>')

response = requests.get(url)

response_json = response.json()
for article in response_json["articles"]: 
    print(article["title"])

# Authenticate to Twitter
auth = tweepy.OAuthHandler("<key>", "<key>")
auth.set_access_token("<key>", "<key>")

# Create API object
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
# Create a tweet
#api.update_status("Hello Tweepy")