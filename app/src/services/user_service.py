from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from app.src.db.main import engine
from models.user_model import User, UserCreate, UserResponse, UserUpdate
from core.auth import create_pass_hash, get_curr_user
from datetime import datetime, timezone
import re


def email_validity_checker(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))


# for jwt usage


def get_user_by_id(user_id: str) -> User:
    with Session(engine) as session:

        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found!!")
        return user


def update_user(userUpdate: UserUpdate, current_user: User = Depends(get_curr_user)) -> UserResponse:
    with Session(engine) as session:
        select_query = select(User).where(User.email == current_user.id)
        user = session.exec(select_query).first()

        if not user:
            return HTTPException(status_code=404, detail="User not found!!")

        if userUpdate.name is not None:
            user.name = userUpdate.name
        if userUpdate.email is not None:
            if not email_validity_checker(userUpdate.email):
                raise HTTPException(
                    status_code=422,
                    detail="Invalid email format"
                )
            if userUpdate.email != user.email:
                raise HTTPException(
                    status_code=409,
                    detail="Email already being used"
                )

            user.email = userUpdate.email
        if userUpdate.password is not None:
            user.pass_hash = create_pass_hash(userUpdate.password)

        user.updated_at = datetime.now(timezone.utc)
        print(type(user))

        session.add(user)
        session.commit()
        session.refresh(user)

    return UserResponse.model_validate(user)


def delete_user(current_user: User = Depends(get_curr_user)) -> dict:
    with Session(engine) as session:
        select_query = select(User).where(User.id == current_user.id)
        user = session.exec(select_query).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found!!")

        for shop in user.shops:
            session.delete(shop)

        session.delete(user)
        session.commit()

    return {"detail": "User deleted successfully"}
