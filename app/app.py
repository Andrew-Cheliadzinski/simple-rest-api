from flask import Flask, Response, jsonify, request
from pymongo import MongoClient
from bson import ObjectId, json_util, errors
from werkzeug.exceptions import BadRequest


app = Flask(__name__)

test_client = app.test_client()

client = MongoClient("mongo", 27017, username='root', password='example')
db = client.companies_database
collection = db.companies


@app.route('/companies', methods=['GET'])
def get_list():
    all_companies = collection.find()
    return Response(json_util.dumps(all_companies), mimetype='application/json'), 200


@app.route('/companies', methods=['POST'])
def create_company():

    if request.content_type != 'application/json':
        raise BadRequest('Content-Type не поддерживается.')

    param = request.json
    if param is None:
        return jsonify(message='No data in request.'), 400
    
    try:
        new_company = collection.insert_one(param)
    except Exception as e:
        # app.logger.error(f'Ошибка при вставки компании {e}')
        return jsonify(message='Не удалось создать компанию.'), 500
    
    res = collection.find_one({'_id': new_company.inserted_id})

    
    return Response(json_util.dumps(res), mimetype='application/json'), 201


@app.route('/companies/<company_id>', methods=['PUT'])
def update_company(company_id):
    if request.content_type != 'application/json':
        return jsonify(message='Bad request'), 400
    
    update_data = request.json
    if update_data is None:
        return jsonify(message='Invalid data.')
    
    try:
        oid = ObjectId(company_id)
    except errors.InvalidId:
        return jsonify({'error': 'Invalid company id'}), 400

    
    update_result = collection.update_one(
        {'_id': oid},
        {'$set': update_data}
    )

    if update_result.matched_count == 0:
        return jsonify({'error': 'Company not found.'}), 404 

    updated_company = collection.find_one({'_id': oid})

    return Response(json_util.dumps(updated_company), mimetype='application/json'), 200


if __name__ == '__main__':
    app.run()