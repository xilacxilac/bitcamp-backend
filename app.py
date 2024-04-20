import os

from flask import Flask
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
uri = os.environ.get('MONGO_URI')
client = MongoClient(uri)

db = client['bitcamp2024']
collection = db["pp"]

test = {"name": "bob", "data": "hello world"}

@app.route('/')
def hello_world():
    try:
        collection.insert_one(test)
    except Exception as e:
        print(e)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
