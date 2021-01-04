import jwt
from flask import request, jsonify
from repositories import user as user_repo
from functools import wraps
from models.user import UserInDB, User
from werkzeug.security import check_password_hash,generate_password_hash
from configs import general as configs

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        #try:
        data = jwt.decode(token, configs.SECRET_KEY, algorithms="HS256")

        #roda uma query pra consultar o cara no banco
        #current_user = User.query.filter_by(public_id=data['public_id']).first()
        current_user = user_repo.find_by_username(data['username'])

        if len(current_user) == 0:
            return jsonify({'message' : 'Token is invalid!'}), 401
        # except:
        #     print('cccccccccccc')
        #     return jsonify({'message' : 'Token is invalid!'}), 401

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
    
#def insert_user(user: User):
def insert_user(username: str, password: str, email: str, full_name: str):
    try:
        user_repo.insert(username, password, email, full_name)
    except Exception as e:
        print("insert error: " + str(e))

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, configs.SECRET_KEY, algorithm=configs.ALGORITHM)
#     return encoded_jwt
