from dotenv import load_dotenv
from pymongo import MongoClient
from tweet_pull import get_latest_hashtags, fetch_tweets

import os
import time
import tweepy

load_dotenv()

FIFTEEN_MINUTES = 900
FIVE_MINUTES = 300
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))

dbc = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
# dbc.tweets

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

print("""       
	 Now scraping latest hastags and tweets....
""")

while (True):
	print("Getting new hashtags.")
	latest_hashtags = get_latest_hashtags(api)
	for hashtag in latest_hashtags:
		print("Fetching tweets for hashtag ", hashtag)
		tweets = fetch_tweets(api, hashtag)
		print("Writing tweets to the database.")
		dbc.tweets.my_collection.insert_many(tweets)
		print("Wait 5 minutes for retrieving tweets for the next hashtag.")
		time.sleep(FIVE_MINUTES)
	time.sleep(FIFTEEN_MINUTES)