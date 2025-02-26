import math
from models.shop_model import NearbyShopQuery, ShopResponse, Shop
from models.user_model import User
from typing import List
from sqlmodel import Session, select
from app.src.db.main import engine
from fastapi import HTTPException


def calc_distance_bw_shops(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

    earth_rad = 6371.0

    lat1_toRad = math.radians(lat1)
    lon1_toRad = math.radians(lon1)

    lat2_toRad = math.radians(lat2)
    lon2_toRad = math.radians(lon2)

    diff_lat = lat2_toRad - lat1_toRad
    diff_lon = lon2_toRad - lon1_toRad

    a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1_toRad) * \
        math.cos(lat2_toRad) * math.sin(diff_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = earth_rad * c

    return distance


def find_shops_near(query: NearbyShopQuery) -> List[ShopResponse]:
    with Session(engine) as session:
        statement = select(Shop, User).join(User, Shop.vendor_id == User.id)
        shops_with_vendors = session.exec(statement).all()
        nearby_shops = []

        for shop, vendor in shops_with_vendors:
            distance = calc_distance_bw_shops(
                query.lattitude, query.longitude, shop.lattitude, shop.longitude
            )

            if distance <= query.radius:
                nearby_shops.append((shop, distance, vendor))
        if len(nearby_shops) == 0:
            raise HTTPException(
                status_code=404, detail="No shops found nearby!!")
        nearby_shops.sort(key=lambda x: x[1])
        limited_shops = nearby_shops[:query.limit]

        return [ShopResponse(
                id=shop.id,
                name=shop.name,
                business_type=shop.business_type,
                latitude=shop.lattitude,
                longitude=shop.longitude,
                vendor_name=vendor.name
                ) for shop, _, vendor in limited_shops]
