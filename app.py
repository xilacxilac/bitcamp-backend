from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/data', methods=['GET'])
def get_data():
    # Example: Get data from Firestore
    data = db.collection('collection_name').document('document_id').get().to_dict()
    return jsonify(data)

@app.route('/data', methods=['POST'])
def add_data():
    # Example: Add data to Firestore
    new_data = {'key': 'value'}
    db.collection('collection_name').document().set(new_data)
    return jsonify({'message': 'Data added successfully'})

test = {"name": "bob", "data": "hello world"}

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
