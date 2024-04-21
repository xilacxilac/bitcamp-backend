import os
import uuid

from flask import Flask, jsonify, json, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta

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
    print(request.json)
    print(request)
    group_name = request.args.get('group_name', default="", type=str)
    chore = Chore(request.args)
    dt = datetime.strptime(request.args.get("datetime", default="2000-01-01 01:00", type=str), "%Y-%m-%d %H:%M")

    if group_name != "":
        try:
            client['chores'][group_name].insert_one({"chore": chore, "due_date": dt, "chore_id": uuid.uuid4()})
            return "200"
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/getchorebyid", methods=['GET'])
def get_chore_by_id():
    group_name = request.args.get('group_name', default="", type=str)

    if group_name != "":
        try:
            return client['chores'][group_name].find({"chore_id": request.args.get('chore_id', type=str)})
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/getchoretoday", methods=['GET'])
def get_chore_today():
    group_name = request.args.get('group_name', default="", type=str)

    if group_name != "":
        try:
            now = datetime.now()
            start_of_today = datetime(now.year, now.month, now.day)
            end_of_today = start_of_today + timedelta(days=1)

            query = {"due_date": {"$gte": start_of_today, "$lt": end_of_today}}
            chores_due_today = client['chores'][group_name].find(query)
            result = list(chores_due_today)
            return result
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/getchoretomorrow", methods=['GET'])
def get_chore_tomorrow():
    group_name = request.args.get('group_name', default="", type=str)

    if group_name != "":
        try:
            now = datetime.now()
            start_of_today = datetime(now.year, now.month, now.day) + timedelta(days=1)
            end_of_today = start_of_today + timedelta(days=2)

            query = {"due_date": {"$gte": start_of_today, "$lt": end_of_today}}
            chores_due_today = client['chores'][group_name].find(query)

            result = list(chores_due_today)
            return result
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/deletechore", methods=['POST'])
def delete_chore():
    group_name = request.args.get('group_name', default="", type=str)

    if group_name != "":
        try:
            client['chores'][group_name].delete_one({"chore_id": request.args.get('chore_id', type=str)})
            return "200"
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


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
