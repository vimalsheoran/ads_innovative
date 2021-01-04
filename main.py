from dotenv import load_dotenv

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

try:
	api.verify_credentials()
	print("API Authenticated.")
except Exception as e:
	print(e)
	print("Error in authenticating.")