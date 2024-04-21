import os
import uuid

from flask import Flask, jsonify, json, request
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pytz import timezone

load_dotenv()

app = Flask(__name__)
uri = os.environ.get('MONGO_URI')
cors = CORS(app, supports_credentials=True)
client = MongoClient(uri)

db = client['bitcamp2024']
collection = db["pp"]


def chore_name_exists(group_name, chore_name):
    for x in client['chores'][group_name].find():
        if x["name"] is chore_name:
            return True
    return False


@app.route("/addchore", methods=['POST'])
def add_chore():
    params = request.json
    group_name = params['group_name']
    params['due_date'] = datetime.strptime(request.json['due_date'], "%Y-%m-%d %H:%M")
    params['chore_id'] = str(uuid.uuid4())
    del params['group_name']

    if group_name != "":
        if not chore_name_exists(group_name, params['name']):
            try:
                client['chores'][group_name].insert_one(params)
                return "200"
            except Exception as e:
                print(e)
                return "400"
        else:
            print("Chore Name Exists")
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/getchoretoday", methods=['GET'])
def get_chore_today():
    params = request.args
    group_name = params['group_name']

    if group_name != "":
        try:
            now = datetime.now(timezone('EST'))
            start_of_today = datetime(now.year, now.month, now.day, now.hour, now.minute)
            end_of_today = datetime(now.year, now.month, now.day) + timedelta(days=1)

            query = {"due_date": {"$gte": start_of_today, "$lt": end_of_today}}

            result = []
            chores_due_today = client['chores'][group_name].find(query)
            for x in chores_due_today:
                del x["_id"]
                del x["chore_id"]
                result.append(x)
            return result
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/getchoretomorrow", methods=['GET'])
def get_chore_tomorrow():
    params = request.args
    group_name = params['group_name']

    if group_name != "":
        try:
            now = datetime.now(timezone('EST'))
            start_of_today = datetime(now.year, now.month, now.day) + timedelta(days=1)
            end_of_today = start_of_today + timedelta(days=2)

            query = {"due_date": {"$gte": start_of_today, "$lt": end_of_today}}

            result = []
            chores_due_tomorrow = client['chores'][group_name].find(query)
            for x in chores_due_tomorrow:
                del x["_id"]
                del x["chore_id"]
                result.append(x)
            return result
        except Exception as e:
            print(e)
            return "400"
    else:
        print("No group defined")
        return "400"


@app.route("/deletechore", methods=['POST'])
def delete_chore():
    params = request.json
    group_name = params['group_name']

    if group_name != "":
        try:
            client['chores'][group_name].delete_one({"chore_id": params['chore_id']})
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
