import pytest
from sqlmodel import Session, select
from app.src.models.user_model import User
from app.src.core.auth import create_pass_hash
from app.src.db.main import engine
import uuid


@pytest.fixture
def test_user_data():
    return {
        "id": str(uuid.uuid4()),
        "name": "CRUD Test User",
        "email": "crud_test_user@example.com",
        "pass_hash": create_pass_hash("password123")
    }


def test_create_user(test_user_data):
    user = User(**test_user_data)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Verify user exists
        statement = select(User).where(User.id == user.id)
        db_user = session.exec(statement).first()
        assert db_user is not None
        assert db_user.name == test_user_data["name"]
        assert db_user.email == test_user_data["email"]
        
        # Cleanup
        session.delete(db_user)
        session.commit()


def test_read_user(test_user_data):
    user = User(**test_user_data)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        
        # Read by id
        db_user = session.get(User, user.id)
        assert db_user is not None
        assert db_user.name == test_user_data["name"]
        
        # Read by email
        statement = select(User).where(User.email == test_user_data["email"])
        db_user_by_email = session.exec(statement).first()
        assert db_user_by_email is not None
        assert db_user_by_email.id == user.id
        
        # Cleanup
        session.delete(db_user)
        session.commit()


def test_update_user(test_user_data):
    user = User(**test_user_data)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        
        # Update user
        db_user = session.get(User, user.id)
        db_user.name = "Updated CRUD User"
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        # Verify update
        assert db_user.name == "Updated CRUD User"
        
        # Cleanup
        session.delete(db_user)
        session.commit()


def test_delete_user(test_user_data):
    user = User(**test_user_data)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        user_id = user.id
        
        # Delete user
        db_user = session.get(User, user_id)
        session.delete(db_user)
        session.commit()
        
        # Verify deletion
        deleted_user = session.get(User, user_id)
        assert deleted_user is None
