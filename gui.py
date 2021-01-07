from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template

import json
import mysql.connector
import os
import time

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

mysql = mysql.connector.connect(
	host=MYSQL_HOST,
	user=MYSQL_USER,
	passwd=MYSQL_PASSWORD,
	database="ads_innovative"
)

app = Flask(__name__)

def top_ten_hashtags():
	try:
		query = """SELECT hashtag, count(retweet_count) as rt FROM tweets GROUP BY hashtag ORDER BY rt DESC LIMIT 10"""
		cursor = mysql.cursor()
		cursor.execute(query)
		result = [[hashtag[0], hashtag[1]] for hashtag in cursor]
		return result
	except Exception as e:
		raise e

def mobile_web_user_ratio():
	try:
		query = """SELECT source, count(source) as cnt FROM tweets GROUP BY source ORDER BY cnt"""
		cursor = mysql.cursor()
		cursor.execute(query)
		result = {val[0]: val[1] for val in cursor}
		return result
	except Exception as e:
		raise e

@app.route("/", methods=['GET'])
def main():
	top_hashtags = top_ten_hashtags()
	mobile_v_web = mobile_web_user_ratio()
	mobile_users = int(round((mobile_v_web['mobile']/(mobile_v_web['mobile']+mobile_v_web['web'])) * 100))
	web_users = int(round((mobile_v_web['web']/(mobile_v_web['mobile']+mobile_v_web['web'])) * 100))
	return render_template("index.html", top_hashtags=top_hashtags, mobile_v_web=[mobile_users, web_users])

if __name__ == "__main__":
	app.run(debug=True)