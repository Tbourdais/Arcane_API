from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from create_database import database


#database(1000) #decomment if you want to generate a test database

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_database'
mongo = PyMongo(app)
db = mongo.db


def is_user(user_id):
    """
    Return True if user_id is in the database.
    """
    return (db.users.find_one({"_id" : ObjectId(user_id)}) != None)

def is_estate(estate_id):
    """
    Return True if estate_id is in the database
    """
    return (db.real_estates.find_one({"_id" : ObjectId(estate_id)}) != None)

@app.route('/users/', methods=['POST'])
def add_user():
    """
    Add a user to the database.
    """
    new_user = request.get_json(force=True)
    date = new_user['birth_date']
    day, month, year = int(date[:2]), int(date[3:5]), int(date[6:])
    new_user['birth_date'] = datetime(year, month, day)
    db.users.insert_one(new_user)
    return "User successfully added.", 200


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update the user info.
    """
    if is_user(user_id):
        data = request.get_json()
        db.users.update_one({'_id':ObjectId(user_id)},
                             {'$set' : data}, upsert=False)
        user = db.users.find_one({'_id':ObjectId(user_id)})
        owner_name = user['first_name'] + ' ' + user['last_name']
        db.real_estates.update_many({'owner_id':ObjectId(user_id)},
                                     {'$set': {'owner' : owner_name}})
        return "User info successfully updated.", 200
    else:
        return "Invalid user ID.", 404


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user from the database, along with all his/her real estates.
    """
    if is_user(user_id):
        db.users.delete_one({'_id':ObjectId(user_id)})
        db.real_estates.delete_many({'owner_id':ObjectId(user_id)})
        return "User successfully deleted.", 200
    else:
        return "Invalid user ID.", 404


@app.route('/real_estates/<user_id>', methods=['POST'])
def add_estate(user_id):
    """
    Add a real estate to the user (assuming owner's name is in the request).
    """
    if is_user(user_id):
        real_estate = request.get_json()
        real_estate['owner_id'] = ObjectId(user_id)
        db.real_estates.insert_one(real_estate)
        return "Real estate successfuly added", 200
    else:
        return "Invalid user ID.", 404

    
@app.route('/real_estates/<user_id>/<estate_id>', methods=['PUT'])
def update_estate(user_id, estate_id):
    """
    Modify the real estate if user_id matches the owner_id of the real estate.
    """
    if is_user(user_id) and is_estate(estate_id):
        real_estate = db.real_estates.find_one({'_id' : ObjectId(estate_id)})
        data = request.get_json()
        if user_id == str(real_estate['owner_id']):
            db.real_estates.update_one({'_id' : ObjectId(estate_id)},
                                       {'$set': data}, upsert=False)
            return "Real estate info successfully updated", 200
        else:
            return "You're not allowed to modify this estate.", 405
    elif not(is_user(user_id)):
        return "Invalid user ID.", 404
    else:
        return "Invalid real estate ID.", 404


@app.route('/real_estates/<user_id>/<estate_id>', methods=['DELETE'])
def delete_estate(user_id, estate_id):
    """
    Delete the real estate if user_id corresponds to owner_id.
    """
    if is_user(user_id) and is_estate(estate_id):
        real_estate = db.real_estates.find_one({'_id' : ObjectId(estate_id)})
        if user_id == str(real_estate['owner_id']):
            db.real_estates.delete_one({'_id' : ObjectId(estate_id)})
            return "Real estate successfully deleted.", 200
        else:
            return "You're not allowed to delete this estate.", 405
    elif not(is_user(user_id)):
        return "Invalid user ID.", 404
    else:
        return "Invalid real estate ID.", 404

        
@app.route('/real_estates/<city>', methods=['GET'])
def get_estate(city):
    """
    Return all the real estates in a given city.
    """
    if (db.real_estates.find({'city':city}).count() > 0):
        result = {}
        for i, estate in enumerate(db.real_estates.find({'city':city})):
            del estate['owner_id']
            del estate['_id']
            key = 'estate_' + str(i)
            result[key] = estate
        return jsonify(result), 200
    else:
        return f"No real estate in {city}.", 404


if __name__ == '__main__':
    app.run(debug=False)
        