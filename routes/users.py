from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi import FastAPI, Body
from models.users import UserSchema, UserLoginSchema, users
from models.auth import AuthHandler

user_router = APIRouter(
    tags=["Users"]
)

@user_router.post('user/register', status_code=201)
def register(scheme: UserSchema):
    if any(x['username'] == UserSchema.username for x in users):
        raise HTTPException(status_code=400, detail='Username sudah diambil!')
    hashed_password = AuthHandler.get_password_hash(UserSchema.password)
    users.append({
        'full_name': UserSchema.fullname,
        'username': UserSchema.username,
        'password': hashed_password
    })
    return {}

@user_router.post('user/login')
def login(scheme: UserLoginSchema):
    user = None
    for x in users:
        if x['username'] == UserLoginSchema.username:
            user = x
            break
    
    if (user is None):
        raise HTTPException(status_code=401, detail='Username tidak terdaftar!')
    
    if (not UserLoginSchema.password, user['password']):
        raise HTTPException(status_code=401, detail='Username atau password salah!')
    
    token = AuthHandler.encode_token(user['username'])
    return {'token': token}