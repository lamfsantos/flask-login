from repositories.user import find_by_username, insert
from typing import Optional
from datetime import datetime, timedelta
from configs import general as configs
from models.user import User, UserInDB
from models.token import Token, TokenData
from jose import JWTError, jwt
from flask import make_response
from fastapi import Depends

def get_password_hash(password):
    return configs.pwd_context.hash(password)

def insert_user(username: str, password: str, email: str, full_name: str):
    try:
        insert(username, get_password_hash(password), email, full_name)
    except Exception as e:
        print("insert error: " + str(e))

def verify_password(plain_password, hashed_password):
    return configs.pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    user = find_by_username(username)
    if len(user) > 0:
        user_dict = list_to_dict(user)[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, configs.SECRET_KEY, algorithm=configs.ALGORITHM)
    return encoded_jwt

def list_to_dict(users_list: list):
    users_dict = {}

    for user in users_list:
        users_dict[user[0]] = {
            "username": user[0],
            "fullname": user[1],
            "email": user[2],
            "hashed_password": user[3],
            "disabled": (False if user[4]==0 else True)
        }
    #users_dict['create_access_token'] = {'name': 'luiz'}
    return users_dict

#ldiar com esse primeiro na rota
def get_current_user(token: str = Depends(configs.oauth2_scheme)):
    credentials_exception = make_response(
        "Could not validate credentials",
        401,
        {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        return credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        return credentials_exception
    return user

def get_current_active_user(current_user: User):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
