import os

from tweepy import OAuthHandler
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()

print('Loading .env variables from', ENV_FILE)

load_dotenv(ENV_FILE)

consumer_key = os.getenv("API_KEY")
consumer_key_secret = os.getenv("API_SECRET_KEY")
access_token = os.getenv('ACCESS_TOKEN')
access_secret_key = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_secret_key)
