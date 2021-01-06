from dotenv import load_dotenv
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

with db.tweets.my_collection.watch() as stream:
	while stream.alive:
		change = stream.try_next()
		if change is not None:
			print(change)
			continue
		time.sleep()