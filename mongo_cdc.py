from dotenv import load_dotenv
from pymongo import MongoClient

import boto3
import json
import os
import time

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
sqs = boto3.client(
	"sqs", 
	aws_access_key_id=AWS_ACCESS_KEY,
	aws_secret_access_key=AWS_SECRET_KEY 
)

queue_url = sqs.get_queue_url(QueueName="ads-innovative")

print ("Connected to queue: " + "ads-innovative")
print("Queue URL: " + queue_url['QueueUrl'])

def get_insert_val(document):
	return json.dumps({
		'created_at': document['created_at'],
		'text': document['text'],
		'source': document['source'],
		'place': document['place'],
		'is_quote_status': document['is_quote_status'],
		'retweet_count': document['retweet_count'],
		'favorite_count': document['favorite_count'],
		'possibly_sensitive': document['possibly_sensitive'],
		'language': document['language'],
		'id': document['id'],
		'timestamp': document['timestamp'],
		'hashtag': document['hashtag']
	})

with db.tweets.my_collection.watch() as stream:
	while stream.alive:
		change = stream.try_next()
		if change is not None:
			print("Emitting Change: " + change['_id']['_data'])
			sqs.send_message(
				QueueUrl=queue_url['QueueUrl'],
				MessageBody=get_insert_val(change['fullDocument'])
			)
		time.sleep(10)