from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import bcrypt
from bson import ObjectId

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'supersecret123'
app.config['JWT_ACCES_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['diskusjonsforum']

users_col = db['users']
threads_col = db['threads']
comments_col = db['comments']

@app.route('/api/register', methods = ['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    name = data.get('name', '').strip()

    if not username or not password or not name:
        return jsonify({'error': 'Alle feltene må fylles ut'}), 400
    if users_col.find_one({'username': username}):
        return jsonify({'error': 'Brukernavnet er allerede tatt'}), 400
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_col.insert_one({
        'username': username,
        'password': hashed,
        'name': name,
        'role': 'user',
        'created_at': datetime.now(timezone.utc)
    })

    token = create_access_token(identity={'username': username, 'role': 'user', 'name': name})
    return jsonify({'token': token, 'username': username, 'role': 'user', 'name': name}), 201

@app.route('/api/login', methods = ['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = users_col.find_one({'username': username})
    if not user or not bcrypt.checkpw(password.encode(), user['password']):
        return jsonify({'error': 'Feil brukernavn eller passord'}), 401
    
    token = create_access_token(identity = {
        'username': user['username'],
        'role': user['role'],
        'name': user['name']
    })
    return jsonify({'token': token, 'username': user['username'], 'role': user['role'], 'name': user['name']})

