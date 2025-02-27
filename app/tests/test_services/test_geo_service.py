import pytest
from app.src.services.geo_service import calc_distance_bw_shops, find_shops_near
from app.src.models.shop_model import NearbyShopQuery, Shop
from app.src.models.user_model import User
from app.src.core.auth import create_pass_hash
from app.src.db.main import engine
from sqlmodel import Session
import uuid


@pytest.fixture
def setup_shops():
    # Create a test user
    user = User(
        id=str(uuid.uuid4()),
        name="Geo Test User",
        email="geo_test@example.com",
        pass_hash=create_pass_hash("password123")
    )

    with Session(engine) as session:
        session.add(user)
        session.commit()

        shops = [
            Shop(
                name="Shop Near Origin",
                business_type="Test",
                lattitude=0.01,  # Very close to origin
                longitude=0.01,
                vendor_id=user.id
            ),
            Shop(
                name="Shop Far Origin",
                business_type="Test",
                lattitude=10.0,  # Far from origin
                longitude=10.0,
                vendor_id=user.id
            ),
            Shop(
                name="Shop Medium Origin",
                business_type="Test",
                lattitude=1.0,  # Medium distance from origin
                longitude=1.0,
                vendor_id=user.id
            )
        ]

        for shop in shops:
            session.add(shop)

        session.commit()
        yield user

        # Cleanup
        for shop in shops:
            session.delete(shop)
        session.delete(user)
        session.commit()


def test_calc_distance_bw_shops():
    # Test points with known distance
    # New York to Los Angeles ≈ 3,940 km
    ny_lat, ny_lon = 40.7128, -74.0060
    la_lat, la_lon = 34.0522, -118.2437

    distance = calc_distance_bw_shops(ny_lat, ny_lon, la_lat, la_lon)

    # Approximate distance with some tolerance
    assert 3900 < distance < 4000

    # Same point should have zero distance
    assert calc_distance_bw_shops(ny_lat, ny_lon, ny_lat, ny_lon) < 0.01


def test_find_shops_near(setup_shops):
    # Search at origin with small radius
    query = NearbyShopQuery(
        lattitude=0.0,
        longitude=0.0,
        radius=2.0,  # Small radius in km
        limit=10
    )

    nearby_shops = find_shops_near(query)

    # Should find the closest shop only
    assert len(nearby_shops) == 1
    assert nearby_shops[0].name == "Shop Near Origin"

    # Search with larger radius
    query.radius = 200.0
    nearby_shops = find_shops_near(query)

    # Should find at least 2 shops, sorted by distance
    assert len(nearby_shops) >= 2
    assert nearby_shops[0].name == "Shop Near Origin"  # Closest first
    # Medium distance second
    assert nearby_shops[1].name == "Shop Medium Origin"
