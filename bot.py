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
    print(twitter_api.verify_credentials())
    print("Successfully logged in")
except tweepy.TweepError as e:
    print(e)
except Exception as e:
    print(e)

tweets_listener = StreamListener(api)
tweet_stream = tweepy.Stream(api.auth, tweets_listener)
tweet_stream.filter(track=["#100DaysOfCode", "#30DaysOfCode"], languages=["en"])
