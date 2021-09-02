from flask import Flask, request
import logging
import os

import userLoginTool
db_name = os.environ['DB_NAME']
db_connection_string = os.environ['DB_CONNECTION_STRING']

from userLoginTool import LoginNOut
l = LoginNOut(db_name, db_connection_string)

import jwt

logger = logging.getLogger("restfulapi")
app = Flask(__name__)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return {
            'error': 'miss username or password in the request data',
            'data': None
        }
    username = data['username']
    password = data['password']
    token = l.get_token(username, password)
    return {
        'error': None,
        'data': token
    }

@app.route('/verifyToken', methods=["GET"])
def verifyToken():
    username = l.varify_token(request.headers.get('access-token'))
    if username is None:
        return {
            'error': 'please login first',
            'data': None
        }
    return {
        'error': None,
        'data': {
            'username': username
        }
    }

@app.route('/register', methods=["POST"])
def register():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return {
            'error': 'miss username or password in the request data',
            'data': None
        }
    username = data['username']
    password = data['password']
    try:
        l.register_user(username, password)
        return {
            'error': None,
            'data': 'success'
        }
    except userLoginTool.UserError as e:
        return {
            'error': 'user already exists',
            'data': None
        }

@app.route('/logout', methods=["GET"])
def logout():
    username = l.varify_token(request.headers.get('access-token'))
    if username is None:
        return {
            'error': 'please login first',
            'data': None
        }
    l.clear_token(username)
    return {
        'error': None,
        'data': f'logout success: {username}'
    }