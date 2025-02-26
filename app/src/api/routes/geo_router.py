from fastapi import APIRouter, Depends, Path, status
from typing import List
from models.shop_model import NearbyShopQuery, ShopResponse
from services.geo_service import find_shops_near

geo_router = APIRouter()


@geo_router.post("/search")
def search_nearby_shops(userquery: NearbyShopQuery) -> List[ShopResponse]:
    return find_shops_near(query=userquery)
