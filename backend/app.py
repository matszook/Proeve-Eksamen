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
