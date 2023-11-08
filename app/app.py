from flask import Flask, Response, jsonify, request
from pymongo import MongoClient
from bson import ObjectId, json_util, errors
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

test_client = app.test_client()

client = MongoClient("mongo", 27017, username=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))
db = client.virtualmem_database
collection = db.virtualmem


@app.route('/memory', methods=['GET'])
def get_list():
    all_companies = collection.find()
    return Response(json_util.dumps(all_companies), mimetype='application/json'), 200


@app.route('/memory', methods=['POST'])
def create_company():

    if request.content_type != 'application/json':
        raise BadRequest('Content-Type is not supported.')

    param = request.json
    if param is None:
        return jsonify(message='No data in request.'), 400
    
    try:
        new_item = collection.insert_one(param)
    except Exception as e:
        return jsonify(message='Failed to create a record.'), 500
    
    res = collection.find_one({'_id': new_item.inserted_id})
    
    return Response(json_util.dumps(res), mimetype='application/json'), 201


@app.route('/memory/<item_id>', methods=['PUT'])
def update_company(item_id):
    if request.content_type != 'application/json':
        return jsonify(message='Bad request'), 400
    
    update_data = request.json
    if update_data is None:
        return jsonify(message='Invalid data.')
    
    try:
        oid = ObjectId(item_id)
    except errors.InvalidId:
        return jsonify({'error': 'Invalid item id'}), 400

    
    update_result = collection.update_one(
        {'_id': oid},
        {'$set': update_data}
    )

    if update_result.matched_count == 0:
        return jsonify({'error': 'Item not found.'}), 404 

    updated_item = collection.find_one({'_id': oid})

    return Response(json_util.dumps(updated_item), mimetype='application/json'), 200

