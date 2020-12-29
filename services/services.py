import jwt
from flask import request, jsonify
from repositories import user as user_repo
from functools import wraps
from models.user import UserInDB, User
from werkzeug.security import check_password_hash,generate_password_hash

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])

            #roda uma query pra consultar o cara no banco
            #current_user = User.query.filter_by(public_id=data['public_id']).first()
            current_user = user_repo.find_by_username(data['username'])

            if len(current_user) == 0:
                return jsonify({'message' : 'Token is invalid!'}), 401
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def get_user(username: str):
    try:
        user = user_repo.find_by_username(username)
        if len(user) > 0:
            user_dict = list_to_dict(user)[username]
            return UserInDB(**user_dict)
    except Exception as e:
        raise e

def list_to_dict(users_list: list):
    users_dict = {}

    for user in users_list:
        users_dict[user[0]] = {
            "username": user[0],
            "full_name": user[1],
            "email": user[2],
            "hashed_password": user[3],
            "disabled": (False if user[4]==0 else True)
        }
    #users_dict['create_access_token'] = {'name': 'luiz'}
    return users_dict

def compare_password_hash(password_hash: str, password_unsalted: str):
    return check_password_hash(password_hash, password_unsalted)