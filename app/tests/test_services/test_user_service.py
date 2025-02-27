import pytest
from app.src.services.user_service import get_user_by_id, update_user, delete_user
from app.src.models.user_model import UserUpdate
from app.src.core.auth import create_pass_hash
from app.src.db.main import engine
from sqlmodel import Session, select
from app.src.models.user_model import User
import uuid


@pytest.fixture
def test_user():
    user = User(
        id=str(uuid.uuid4()),
        name="Service Test User",
        email="service_test_user@example.com",
        pass_hash=create_pass_hash("password123")
    )
    
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        yield user
        
        # Cleanup
        session.delete(user)
        session.commit()


def test_get_user_by_id(test_user):
    user = get_user_by_id(test_user.id)
    assert user.id == test_user.id
    assert user.name == test_user.name
    assert user.email == test_user.email


def test_update_user(test_user):
    user_update = UserUpdate(name="Updated Service User")
    updated_user = update_user(user_update, test_user)
    assert updated_user.name == "Updated Service User"
    
    # Verify in the database
    with Session(engine) as session:
        db_user = session.get(User, test_user.id)
        assert db_user.name == "Updated Service User"


def test_delete_user(test_user):
    # Add a shop to the user to test cascade delete
    from app.src.models.shop_model import Shop
    with Session(engine) as session:
        shop = Shop(
            name="Test Shop for Delete",
            business_type="Test",
            lattitude=0.0,
            longitude=0.0,
            vendor_id=test_user.id
        )
        session.add(shop)
        session.commit()
    
    # Delete the user
    delete_user(test_user)
    
    # Check if user exists
    with Session(engine) as session:
        user = session.get(User, test_user.id)
        assert user is None
        
        # Check if shop was also deleted
        statement = select(Shop).where(Shop.vendor_id == test_user.id)
        shop = session.exec(statement).first()
        assert shop is None
