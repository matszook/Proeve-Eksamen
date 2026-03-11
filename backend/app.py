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

@app.route('/api/threads', methods = ['GET'])
def get_threads():
    threads = list(threads_col.find().sort('created_at', -1))
    for t in threads:
        t['_id'] = str(t['_id'])
        t['comment_count'] = comments_col.count_documents({'thread_id': t['_id']})
    return jsonify(threads)

@app.route('/api/threads', methods = ['POST'])
@jwt_required()
def create_thread():
    identity = get_jwt_identity()
    if identity['role'] == 'guest':
        return jsonify({'error': 'Gjester kan ikke utføre denne handlingen'}), 403
    data = request.json
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Tittel og innhold er påkrevd'}), 400
    
    thread = {
        'title': title,
        'content': content,
        'author': identity['username'],
        'author_name': identity['name'],
        'role': identity['role'],
        'created_at': datetime.now(timezone.utc)
    }
    result = threads_col.insert_one(thread)
    thread['_id'] = str(result.inserted_id)
    return jsonify(thread), 201

@app.route('/api/threads/<thread_id>', methods = ['GET'])
def get_thread(thread_id):
    try:
        thread = threads_col.find_one({'_id': ObjectId(thread_id)})
        if not thread:
            return jsonify({'error': 'Tråd ikke funnet'}), 404
        thread['_id'] = str(thread['_id'])
        comments = list(comments_col.find({'thread_id': thread_id}).sort('created_at', 1))
        for c in comments:
            c['_id'] = str(c['_id'])
        return jsonify({'thread': thread, 'comments': comments})
    except:
        return jsonify({'error': 'Ugyldig ID'}), 400

@app.route('/api/threads/<thread_id>', methods=['DELETE'])
@jwt_required()
def delete_thread(thread_id):
    identity = get_jwt_identity()
    try:
        thread = threads_col.find_one({'_id': ObjectId(thread_id)})
        if not thread:
            return jsonify({'error': 'Tråd ikke funnet'}), 404
        if thread['author'] != identity['username'] and identity['role'] not in ['admin', 'moderator']:
            return jsonify({'error': 'Ingen tilgang'}), 403
        threads_col.delete_one({'_id': ObjectId(thread_id)})
        comments_col.delete_many({'thread_id': thread_id})
        return jsonify({'message': 'Tråd slettet'})
    except:
        return jsonify({'error': 'Ugyldig ID'}), 400

@app.route('/api/threads/<thread_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(thread_id):
    identity = get_jwt_identity()
    if identity['role'] == 'guest':
        return jsonify({'error': 'Gjester kan ikke utføre denne handlingen'}), 403
    data = request.json
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'error': 'Kommentar kan ikke være tom'}), 400

    comment = {
        'thread_id': thread_id,
        'content': content,
        'author': identity['username'],
        'author_name': identity['name'],
        'role': identity['role'],
        'created_at': datetime.now(timezone.utc)
    }
    result = comments_col.insert_one(comment)
    comment['_id'] = str(result.inserted_id)
    return jsonify(comment), 201

@app.route('/api/threads/<thread_id>/comments/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(thread_id, comment_id):
    identity = get_jwt_identity()
    try:
        comment = comments_col.find_one({'_id': ObjectId(comment_id)})
        if not comment:
            return jsonify({'error': 'Kommentar ikke funnet'}), 404
        if comment['author'] != identity['username'] and identity['role'] not in ['admin', 'moderator']:
            return jsonify({'error': 'Ingen tilgang'}), 403
        comments_col.delete_one({'_id': ObjectId(comment_id)})
        return jsonify({'message': 'Kommentar slettet'})
    except:
        return jsonify({'error': 'Ugyldig ID'}), 400

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Ingen tilgang'}), 403
    users = list(users_col.find({}, {'password': 0}))
    for u in users:
        u['_id'] = str(u['_id'])
    return jsonify(users)

