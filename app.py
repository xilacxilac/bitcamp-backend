import os

from flask import Flask, jsonify, json, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

from Chore import Chore

load_dotenv()

app = Flask(__name__)
uri = os.environ.get('MONGO_URI')
cors = CORS(app, supports_credentials=True)
client = MongoClient(uri)

db = client['bitcamp2024']
collection = db["pp"]


@app.route("/addchore", methods=['POST'])
def add_chore():
    group_name = request.args.get('group_name', default="", type=str)
    chore = Chore(request.args)

    if group_name != "":
        try:
            client['chores'][group_name].insert_one({"chore": chore})
        except Exception as e:
            print(e)
    else:
        print("No group defined")

@app.route("/getchore", methods=['GET'])
def get_chore():
    return


@app.route("/deletechore", methods=['POST'])
def delete_chore():
    return


@app.route('/test')
def test():
    return json.dumps({"name": "bob", "data": "hello world"})


@app.route('/')
def index():
    try:
        collection.insert_one({"name": "bob", "data": "hello world"})
    except Exception as e:
        print(e)
    return "Backend is Up"
