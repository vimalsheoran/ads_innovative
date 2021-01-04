from dotenv import load_dotenv
from tweet_pull import get_latest_hashtags, fetch_tweets

import os
import tweepy

load_dotenv()

CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# latest_hashtags = get_latest_hashtags(api)
fetch_tweets(api, "#MondayMotivation")

print(latest_hashtags)