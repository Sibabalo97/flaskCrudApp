
from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/profiles'
app.config['JWT_SECRET_KEY'] = "mongodb+srv://sibabalomaqiy:V47NAhaFpxiI3e6v@cluster0.wdlzs0r.mongodb.net/?retryWrites=true&w=majority"

mongo = PyMongo(app)
jwt = JWTManager(app)

# Data Models
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()

class Profile:
    def __init__(self, id_user, name, surname, phone):
        self.id_user = id_user
        self.name = name
        self.surname = surname
        self.phone = phone
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(email, password)
    mongo.db.users.insert_one({
        'email': new_user.email,
        'password': new_user.password,
        'created': new_user.created,
        'updated': new_user.updated
    })

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = mongo.db.users.find_one({'email': email, 'password': password})
    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({'access_token': access_token}), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    profiles = mongo.db.profiles.find({'id_user': current_user_id})
    return jsonify([{'id_user': profile['id_user'], 'name': profile['name'], 'surname': profile['surname'], 'phone': profile['phone']} for profile in profiles]), 200

@app.route('/profiles', methods=['GET'])
def list_profiles():
    profiles = mongo.db.profiles.find()
    return jsonify([{'id_user': profile['id_user'], 'name': profile['name'], 'surname': profile['surname'], 'phone': profile['phone']} for profile in profiles]), 200

@app.route('/profile', methods=['POST'])
@jwt_required()
def create_profile():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    name = data.get('name')
    surname = data.get('surname')
    phone = data.get('phone')

    new_profile = Profile(current_user_id, name, surname, phone)
    mongo.db.profiles.insert_one({
        'id_user': new_profile.id_user,
        'name': new_profile.name,
        'surname': new_profile.surname,
        'phone': new_profile.phone,
        'created': new_profile.created,
        'updated': new_profile.updated
    })

    return jsonify({'message': 'Profile created successfully'}), 201

@app.route('/profile/<string:profile_id>', methods=['PUT'])
@jwt_required()
def update_profile(profile_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    name = data.get('name')
    surname = data.get('surname')
    phone = data.get('phone')

    mongo.db.profiles.update_one({'_id': profile_id, 'id_user': current_user_id}, {'$set': {
        'name': name,
        'surname': surname,
        'phone': phone,
        'updated': datetime.utcnow()
    }})

    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/profile/<string:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(profile_id):
    current_user_id = get_jwt_identity()
    try:
        # Convert profile_id to ObjectId
        profile_id = ObjectId(profile_id)
    except Exception as e:
        return jsonify({'message': str(e)}), 400  # Return error message if conversion fails

    # Delete the profile
    result = mongo.db.profiles.delete_one({'_id': profile_id, 'id_user': current_user_id})
    
    if result.deleted_count == 1:
        return jsonify({'message': 'Profile deleted successfully'}), 200
    else:
        return jsonify({'message': 'Profile not found or you do not have permission to delete it'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5003)






