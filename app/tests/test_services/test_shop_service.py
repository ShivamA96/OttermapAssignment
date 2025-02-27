import pytest
from app.src.services.shop_service import create_shop, get_shop_by_id, get_shops_by_vendor, update_shop, delete_shop
from app.src.models.shop_model import ShopCreate, ShopUpdate
from app.src.models.user_model import User
from app.src.core.auth import create_pass_hash
from app.src.db.main import engine
from sqlmodel import Session, select
from app.src.models.shop_model import Shop
import uuid


@pytest.fixture
def test_user():
    user = User(
        id=str(uuid.uuid4()),
        name="Shop Service Test User",
        email="shop_service_test@example.com",
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


@pytest.fixture
def test_shop(test_user):
    shop_create = ShopCreate(
        name="Test Service Shop",
        business_type="Test",
        latitude=38.8951,
        longitude=-77.0364
    )
    shop = create_shop(shop_create, test_user)
    yield shop
    
    # Cleanup happens with user deletion


def test_create_shop(test_user):
    shop_create = ShopCreate(
        name="New Service Shop",
        business_type="Retail",
        latitude=40.7128,
        longitude=-74.0060
    )
    shop = create_shop(shop_create, test_user)
    assert shop.name == "New Service Shop"
    assert shop.business_type == "Retail"
    assert shop.latitude == 40.7128
    assert shop.longitude == -74.0060
    assert shop.vendor_name == test_user.name


def test_get_shop_by_id(test_shop):
    shop = get_shop_by_id(test_shop.id)
    assert shop.id == test_shop.id
    assert shop.name == test_shop.name


def test_get_shops_by_vendor(test_user, test_shop):
    shops = get_shops_by_vendor(test_user)
    assert len(shops) >= 1
    assert any(shop.id == test_shop.id for shop in shops)


def test_update_shop(test_user, test_shop):
    shop_update = ShopUpdate(name="Updated Service Shop")
    updated_shop = update_shop(test_shop.id, shop_update, test_user)
    assert updated_shop.name == "Updated Service Shop"
    
    # Verify in database
    with Session(engine) as session:
        statement = select(Shop).where(Shop.id == test_shop.id)
        db_shop = session.exec(statement).first()
        assert db_shop.name == "Updated Service Shop"


def test_delete_shop(test_user, test_shop):
    result = delete_shop(test_shop.id, test_user)
    assert "detail" in result
    
    # Verify deletion
    with Session(engine) as session:
        statement = select(Shop).where(Shop.id == test_shop.id)
        shop = session.exec(statement).first()
        assert shop is None
