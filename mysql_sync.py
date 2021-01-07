#!/usr/bin/python3

from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

import boto3
import json
import mysql.connector
import os
import time

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
mysql = mysql.connector.connect(
	host=MYSQL_HOST,
	user=MYSQL_USER,
	passwd=MYSQL_PASSWORD,
	database="ads_innovative"
)

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
sqs = boto3.client(
	"sqs", 
	aws_access_key_id=AWS_ACCESS_KEY,
	aws_secret_access_key=AWS_SECRET_KEY 
)

queue_url = sqs.get_queue_url(QueueName="ads-innovative")

print("Service Started At: {}".format(datetime.now().strftime("%Y:%m:%d %H:%M:%S")))
print("Connected to MongoDB...")
print("Connected to SQS...")
print("Connected to MySQL...")

query = """
	INSERT INTO tweets(
		created_at, 
		source, 
		is_quote_status, 
		retweet_count, 
		favorite_count, 
		possibly_sensitive, 
		language,
		id,
		timestamp,
		hashtag
	) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
"""

while(True):
	response = sqs.receive_message(
		QueueUrl=queue_url['QueueUrl'], 
		AttributeNames=['All'], 
		MaxNumberOfMessages=10
	)
	cur = mysql.cursor()
	entries = []
	for message in response['Messages']:
		try:
			body = json.loads(message['Body'])
			cur.execute(query.format(
				body['created_at'],
				body['source'],
				body['is_quote_status'],
				body['retweet_count'],
				body['favorite_count'],
				body['possibly_sensitive'],
				body['language'],
				body['id'],
				body['timestamp'],
				body['hashtag']
			))
			mysql.commit()
			entries.append({
				'Id': message['MessageId'], 
				'ReceiptHandle': message['ReceiptHandle']
			})
		except Exception as e:
			print("Unable to process entry. Time: {}".format(datetime.now().strftime("%Y:%m:%d %H:%M:%S")))
			print(body)
	try:
		sqs.delete_message_batch(QueueUrl=queue_url['QueueUrl'], Entries=entries)
	except Exception as e:
		pass
	print("Consumed 10 messages at {}".format(datetime.now().strftime("%Y:%m:%d %H:%M:%S")))
	time.sleep(5)
