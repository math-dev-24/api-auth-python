from core.JWT import JWT
from core.Tools import Tools
from models.bdd import db
from models.userClass import User


class Auth:

    @staticmethod
    def create_user(json: dict):
        username = json.get('username')
        password = json.get('password')
        email = json.get('email')
        user = User.get_user_by_email(email)
        if user:
            return {'code': 400, 'message': 'Error in creating user'}

        if Tools.email_validator(email):
            hashed_password: str = Tools.hash_password(password)
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return {'code': 200, 'message': 'User created successfully'}
        else:
            return {'code': 400, 'message': 'Error in creating user'}

    @staticmethod
    def login(email: str, password: str):
        user = User.get_user_by_email(email)
        if not user:
            return {'code': 401, 'message': 'Error in logging in'}
        if Tools.compare_passwords(password, user.password):
            header = {'alg': 'HS256', 'typ': 'JWT'}
            payload = {'user_id': user.id, "email": user.email, "username": user.username}
            token = JWT().generate_token(header=header, payload=payload)
            return {'code': 200, 'message': {'token': token, "message": 'User logged in successfully'}}
        else:
            return {'code': 401, 'message': 'error in logging in'}

    @staticmethod
    def get_users():
        return User.get_users()

    @staticmethod
    def is_valid(token: str):
        return JWT.is_valid(token)

    @staticmethod
    def check_token(token: str):
        return JWT().check_validity(token)

    @staticmethod
    def generate_token(token: str):
        payload = JWT().get_payload(token)
        print(payload)
        email = payload['email']
        user = User.get_user_by_email(email)
        if not user:
            return {'code': 401, 'message': 'Invalid email'}
        else:
            header = {'alg': 'HS256', 'typ': 'JWT'}
            payload = {'user_id': user.id, "email": user.email, "username": user.username}
            token = JWT().generate_token(header=header, payload=payload)
            return {'code': 200, 'message': {'token': token, "info": 'Token generated successfully'}}