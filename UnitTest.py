from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database to store user profiles
profiles_db = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Add user to the database (dummy implementation)
    email = data['email']
    password = data['password']
    profiles_db[email] = {'email': email, 'password': password}
    
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.json
    if 'id_user' not in data or 'name' not in data or 'surname' not in data or 'phone' not in data:
        return jsonify({'error': 'Missing required fields'}), 422
    
    # Add profile to the database (dummy implementation)
    id_user = data['id_user']
    profiles_db[id_user] = data
    
    return jsonify({'message': 'Profile created successfully'}), 200

@app.route('/profile/<id>', methods=['DELETE'])
def delete_profile(id):
    if id not in profiles_db:
        return jsonify({'error': 'Profile not found'}), 404
    
    # Delete profile from the database (dummy implementation)
    del profiles_db[id]
    
    return jsonify({'message': 'Profile deleted successfully'}), 200


import unittest


class TestAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_register_endpoint(self):
        # Test the registration endpoint
        data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 200)

    def test_profile_creation_endpoint(self):
        # Test the profile creation endpoint
        data = {
            "id_user": "65d134b9aaf3e8e279108678",
            "name": "John",
            "surname": "Doe",
            "phone": "1234567890"
        }
        response = self.app.post('/profile', json=data)
        self.assertEqual(response.status_code, 200)

    def test_profile_deletion_endpoint(self):
        # Test the profile deletion endpoint
        profile_id = "65d134b9aaf3e8e279108678"
        response = self.app.delete(f'/profile/{profile_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
