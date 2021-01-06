from datetime import datetime

# WOEID for fetching trends from Mumbai
WOEID = 2295411

def get_latest_hashtags(api):
	try:
		trends = api.trends_place(id=WOEID)
		for value in trends:
			return [trend['name'] for trend in value['trends']]
	except Exception as e:
		raise e

def fetch_tweets(api, hashtag):
	try:
		tweets = api.search(q=hashtag, count=100)
		tweet_list = []
		num_tweets = 0
		for tweet in tweets:
			t = {
				'created_at': datetime.strptime(
					tweet._json['created_at'], 
					"%a %b %d %H:%M:%S %z %Y"
				).strftime("%Y-%m-%d %H:%M:%S"),
				'text': tweet._json['text'],
				'source': "web" if "Web App" in tweet._json['source'] else "mobile",
				'place': tweet._json['place'],
				'is_quote_status': tweet._json['is_quote_status'],
				'retweet_count': tweet._json['retweet_count'],
				'favorite_count': tweet._json['favorite_count'],
				'possibly_sensitive': tweet._json.get('possibly_sensitive'),
				'language': tweet._json['lang'],
				'id': tweet._json['id'],
				'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				'hashtag': hashtag
			}
			tweet_list.append(t)
		return tweet_list
	except Exception as e:
		raise e
