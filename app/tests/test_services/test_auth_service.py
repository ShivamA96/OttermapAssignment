import pytest
import asyncio
from app.src.services.auth_service import register_user, login_user, email_validity_checker
from app.src.models.user_model import UserCreate, UserLogin
from sqlmodel import Session, select
from app.src.models.user_model import User
from app.src.db.main import engine


def test_email_validity_checker():
    assert email_validity_checker("valid@example.com") == True
    assert email_validity_checker("invalid-email") == False
    assert email_validity_checker("another.invalid@") == False


@pytest.fixture
async def registered_user():
    user_create = UserCreate(
        name="Auth Test User",
        email="auth_test_user@example.com",
        password="password123"
    )
    result = await register_user(user_create)
    yield result
    
    # Cleanup
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "auth_test_user@example.com")).first()
        if user:
            session.delete(user)
            session.commit()


@pytest.mark.asyncio
async def test_register_user():
    user_create = UserCreate(
        name="Register Test User",
        email="register_test@example.com",
        password="password123"
    )
    result = await register_user(user_create)
    assert "jwt_token" in result
    assert "token_type" in result
    assert "user_id" in result
    
    # Verify user exists in database
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "register_test@example.com")).first()
        assert user is not None
        assert user.name == "Register Test User"


@pytest.mark.asyncio
async def test_login_user(registered_user):
    user_login = UserLogin(
        email="auth_test_user@example.com",
        password="password123"
    )
    result = await login_user(user_login)
    assert "jwt_token" in result
    assert "token_type" in result
    assert "user_id" in result
