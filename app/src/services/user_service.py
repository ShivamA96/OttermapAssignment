from sqlmodel import Session, select, insert,

from src.db.main import engine
from src.models.user_model import User, UserCreate, UserResponse, UserUpdate


def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
