from flask import Flask, request, jsonify
from core.Auth import Auth
from models.bdd import db
import os


def send_response(code, message):
    return jsonify(message), code


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'db.sqlite')
db.init_app(app)

auth_manager = Auth()

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    return jsonify({'api': {
        "version": '1.0',
        "endpoints": [
            {
                "name": 'users',
                "method": 'GET',
                "description": 'Get all users',
                "parameters": []
            },
            {
                "name": 'user',
                "method": 'POST',
                "description": 'Create user',
                "parameters": [
                    {
                        "name": "email",
                        "required": True
                    },
                    {
                        "name": "username",
                        "required": True
                    },
                    {
                        "name": "password",
                        "required": True
                    }
                ]
            },
            {
                "name": 'auth',
                "method": 'POST',
                "description": 'Authenticate user',
                "parameters": [
                    {
                        "name": 'Authorization',
                        "description": 'Bearer token',
                        "required": True
                    }
                ]
            }
        ]
    }})


@app.route('/users', methods=['GET'])
def users():
    list_users = auth_manager.get_users()
    data = {
        "quantity": len(list_users),
        "users": list_users
    }
    return send_response(200, data)


@app.route('/user', methods=['POST'])
def create_user():
    headers = request.headers
    if headers.get('Content-Type') == 'application/json':
        result = auth_manager.create_user(request.json)
        return send_response(200, result)
    else:
        return send_response(400, {'error': 'Unsupported Content-Type'})


@app.route('/auth', methods=['POST'])
def auth():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1] if "Bearer " in auth_header else None
        print(token)
        if token:
            if auth_manager.is_valid(auth_header):
                return send_response(200, {'auth_token': token})
            else:
                return send_response(400, {'error': 'Invalid token'})
        else:
            return send_response(400, {'error': 'Invalid token'})


@app.route('/validity-token', methods=['POST'])
def validity_token():
    token = request.json.get('token')
    if token:
        if auth_manager.is_valid(token):
            if auth_manager.check_token(token):
                return send_response(200, {'validity': True})
    return send_response(400, {'error': 'Invalid token'})


@app.route('/generate-token', methods=['POST'])
def generate_token():
    token = request.json.get('token')
    if token:
        if auth_manager.check_token(token):
            res: dict = auth_manager.generate_token(token)
            return send_response(res['code'], res['message'])
    return send_response(400, {'error': 'Invalid token'})


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    auth_header = request.headers.get('Content-Type')
    if auth_header and auth_header == 'application/json':
        res: dict = auth_manager.login(email, password)
        return send_response(res['message'], res['message'])
    else:
        return send_response(400, {'error': 'Invalid token'})


if __name__ == '__main__':
    app.run(debug=True)
