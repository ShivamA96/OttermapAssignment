from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from app.src.db.main import engine
from models.user_model import User, UserCreate, UserLogin, UserResponse, UserUpdate
from core.auth import create_pass_hash, get_curr_user, verify_pass, create_access_token
from datetime import datetime, timezone

import re


def email_validity_checker(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))


async def register_user(userCreate: UserCreate):
    hashed_pass = create_pass_hash(userCreate.password)
    user = User(name=userCreate.name,
                email=userCreate.email, pass_hash=hashed_pass)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        jwt_token = await create_access_token(data={"sub": str(user.id)})

    return {"jwt_token": jwt_token, "token_type": "Bearer", "user_id": str(user.id)}


async def login_user(userLogin: UserLogin):
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.email == userLogin.email)).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_pass(userLogin.password, user.pass_hash):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        jwt_token = await create_access_token(data={"user_id": str(user.id)})

    return {
        "jwt_token": jwt_token,
        "token_type": "bearer",
        "user_id": str(user.id)
    }
