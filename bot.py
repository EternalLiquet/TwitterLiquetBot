import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('twitter_api_key')
API_SECRET = os.getenv('twitter_api_secret')
ACCESS_TOKEN = os.getenv('twitter_access_token')
TOKEN_SECRET = os.getenv('twitter_token_secret')

print(f"{API_KEY}, {API_SECRET}, {ACCESS_TOKEN}, {TOKEN_SECRET}")

oauth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oauth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)

api = tweepy.API(oauth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

try:
    api.verify_credentials()
    print("Authentication SUCCESS")
except:
    print("Authentication ERROR")

counter = 1
for tweet in api.search(q="#100DaysOfCode", lang="en", rpp=10):
    print(f"{counter}: {tweet.user.name}:{tweet.text}")
    counter += 1