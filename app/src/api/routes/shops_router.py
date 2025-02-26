from fastapi import APIRouter, Depends, Path, status
from typing import List

from models.shop_model import ShopCreate, ShopResponse, ShopUpdate
from models.user_model import User
from core.auth import get_curr_user
from services.shop_service import (
    create_shop,
    get_shop_by_id,
    get_shops_by_vendor,
    update_shop,
    delete_shop
)

shops_router = APIRouter(
    tags=["shops"]
)


@shops_router.post("/shops", response_model=ShopResponse, status_code=status.HTTP_201_CREATED)
def create_shop_func(
    shop_data: ShopCreate,
    current_user: User = Depends(get_curr_user)
):
    return create_shop(shop_data, current_user)


@shops_router.get("/shops/{shop_id}", response_model=ShopResponse)
def get_shop_func(
    shop_id: str = Path(..., title="The ID of the shop to get")
):
    return get_shop_by_id(shop_id)


@shops_router.get("/shops", response_model=List[ShopResponse])
def get_user_shops_func(
    current_user: User = Depends(get_curr_user)
):
    return get_shops_by_vendor(current_user)


@shops_router.put("/shops/{shop_id}", response_model=ShopResponse)
def update_shop_func(
    shop_update: ShopUpdate,
    shop_id: str = Path(..., title="The ID of the shop to update"),
    current_user: User = Depends(get_curr_user)
):
    return update_shop(shop_id, shop_update, current_user)


@shops_router.delete("/shops/{shop_id}")
def delete_shop_func(
    shop_id: str = Path(..., title="The ID of the shop to delete"),
    current_user: User = Depends(get_curr_user)
):
    return delete_shop(shop_id, current_user)
