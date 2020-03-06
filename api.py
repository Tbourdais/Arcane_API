from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_database'
mongo = PyMongo(app)
db = mongo.db
    
@app.route('/users/', methods=['POST'])
def add_user():
    """
    Add a user to the database.
    """
    new_user = request.get_json(force=True)
    db.users.insert_one(new_user)
    return "User successfully added."

@app.route('/users/<user_id>', methods=['POST'])
def update_user(user_id):
    """
    Update the user info
    """
    data = request.get_json()
    db.users.update_one({'_id':ObjectId(user_id)},
                         {'$set' : data}, upsert=False)
    user = db.users.find_one({'_id':ObjectId(user_id)})
    owner_name = user['first_name'] + ' ' + user['last_name']
    db.real_estates.update_many({'owner_id':ObjectId(user_id)},
                                 {'$set': {'owner' : owner_name}})
    return "User info successfully updated."

@app.route('/users/<user_id>', methods=['POST'])
def add_estate(user_id):
    """
    Add a real estate to the user.
    """
    real_estate = request.get_json()
    real_estate['owner_id'] = ObjectId(user_id)
    db.real_estates.insert_one(real_estate)
    return "Real estate successfuly added"
    
@app.route('/users/<user_id>/<estate_id>', methods=['POST'])
def update_estate(user_id, estate_id):
    """
    Modify the real estate if user_id matches the owner_id of the real estate.
    """
    real_estate = db.real_estates.find_one({'_id' : ObjectId(estate_id)})
    data = request.get_json()
    if user_id == str(real_estate['owner_id']):
        db.real_estates.update_one({'_id' : ObjectId(estate_id)},
                                   {'$set': data}, upsert=False)
        return "Real estate info successfully updated"
    else:
        return "You're not allowed to modify this estate."

@app.route('/users/<city>', methods=['GET'])
def get_estate(city):
    """
    Return all the real estates in a given city.
    """
    result = {}
    for i, estate in enumerate(db.real_estates.find({'city':city})):
        del estate['owner_id']
        del estate['_id']
        key = 'estate_' + str(i)
        result[key] = estate
    return jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=False)
        