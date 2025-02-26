from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from models.user_model import UserCreate, UserResponse, UserUpdate
from services.user_service import update_user, delete_user, get_user_by_id
from core.auth import get_curr_user


user_router = APIRouter()


@user_router.get("/users/{user_id}", response_model=UserResponse)
def get_user_func(user_id):
    return get_user_by_id(user_id)


@user_router.put("/users/", response_model=UserResponse)
def update_current_func(user_update: UserUpdate, current_user: UserResponse = Depends(get_curr_user)):
    return update_user(user_update, current_user)


@user_router.delete("/users/", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_func(current_user: UserResponse = Depends(get_curr_user)):
    delete_user(current_user)
    return {"detail": "User deleted successfully"}
