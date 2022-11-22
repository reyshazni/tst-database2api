from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi import FastAPI, Body
from models.users import UserSchema, UserLoginSchema
# from auth.auth_handler import signJWT

user_router = APIRouter(
    tags=["Users"]
)

# @user_router.post("/user/signup", tags=["user"])
# async def create_user(user: UserSchema = Body(...)):
#     users.append(user) # replace with db call, making sure to hash the password first
#     return signJWT(user.email)
