import pytest
from sqlmodel import Session, select
from app.src.models.shop_model import Shop
from app.src.models.user_model import User
from app.src.core.auth import create_pass_hash
from app.src.db.main import engine
import uuid


@pytest.fixture
def test_vendor():
    vendor = User(
        id=str(uuid.uuid4()),
        name="CRUD Shop Vendor",
        email="shop_crud_vendor@example.com",
        pass_hash=create_pass_hash("password123")
    )
    
    with Session(engine) as session:
        session.add(vendor)
        session.commit()
        session.refresh(vendor)
        yield vendor
        
        # Cleanup
        session.delete(vendor)
        session.commit()


@pytest.fixture
def test_shop_data(test_vendor):
    return {
        "id": str(uuid.uuid4()),
        "name": "CRUD Test Shop",
        "business_type": "Test",
        "lattitude": 42.3601,
        "longitude": -71.0589,
        "vendor_id": test_vendor.id
    }


def test_create_shop(test_shop_data):
    shop = Shop(**test_shop_data)
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)
        
        # Verify shop exists
        statement = select(Shop).where(Shop.id == shop.id)
        db_shop = session.exec(statement).first()
        assert db_shop is not None
        assert db_shop.name == test_shop_data["name"]
        assert db_shop.business_type == test_shop_data["business_type"]
        
        # Cleanup
        session.delete(db_shop)
        session.commit()


def test_read_shop(test_shop_data):
    shop = Shop(**test_shop_data)
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        
        # Read by id
        db_shop = session.get(Shop, shop.id)
        assert db_shop is not None
        assert db_shop.name == test_shop_data["name"]
        
        # Read by vendor_id
        statement = select(Shop).where(Shop.vendor_id == test_shop_data["vendor_id"])
        vendor_shops = session.exec(statement).all()
        assert len(vendor_shops) >= 1
        assert any(s.id == shop.id for s in vendor_shops)
        
        # Cleanup
        session.delete(db_shop)
        session.commit()


def test_update_shop(test_shop_data):
    shop = Shop(**test_shop_data)
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        
        # Update shop
        db_shop = session.get(Shop, shop.id)
        db_shop.name = "Updated CRUD Shop"
        db_shop.business_type = "Updated Type"
        session.add(db_shop)
        session.commit()
        session.refresh(db_shop)
        
        # Verify update
        assert db_shop.name == "Updated CRUD Shop"
        assert db_shop.business_type == "Updated Type"
        
        # Cleanup
        session.delete(db_shop)
        session.commit()


def test_delete_shop(test_shop_data):
    shop = Shop(**test_shop_data)
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        shop_id = shop.id
        
        # Delete shop
        db_shop = session.get(Shop, shop_id)
        session.delete(db_shop)
        session.commit()
        
        # Verify deletion
        deleted_shop = session.get(Shop, shop_id)
        assert deleted_shop is None
