import tweepy
import os
from dotenv import load_dotenv
import json
from streamlistener import StreamListener

load_dotenv()

API_KEY = os.getenv('twitter_api_key')
API_SECRET = os.getenv('twitter_api_secret')
ACCESS_TOKEN = os.getenv('twitter_access_token')
TOKEN_SECRET = os.getenv('twitter_token_secret')

oauth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oauth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)

api = tweepy.API(oauth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

try:
    api.verify_credentials()
    print("Authentication SUCCESS")
except:
    print("Authentication ERROR")

tweets_listener = StreamListener(api)
tweet_stream = tweepy.Stream(api.auth, tweets_listener)
tweet_stream.filter(track=["#100DaysOfCode", "#30DaysOfCode"], languages=["en"])
