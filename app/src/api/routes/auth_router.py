from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from models.user_model import UserCreate, UserResponse, UserLogin
from services.auth_service import register_user, login_user

auth_router = APIRouter(tags=["authentication"])


class TokenedResponse(BaseModel):
    jwt_token: str
    token_type: str
    user_id: str


@auth_router.post("/auth/register", response_model=TokenedResponse)
async def create_user(user: UserCreate):
    return await register_user(user)


@auth_router.post("/auth/login", response_model=TokenedResponse)
async def login_for_jwt_token(userData: UserLogin):
    return await login_user(userData)
