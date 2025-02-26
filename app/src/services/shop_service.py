from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from app.src.db.main import engine
from models.shop_model import Shop, ShopCreate, ShopResponse, ShopUpdate
from datetime import datetime, timezone

from models.user_model import User
from core.auth import get_curr_user
from typing import List


def create_shop(shop_data: ShopCreate, current_user: User = Depends(get_curr_user)) -> ShopResponse:
    with Session(engine) as session:
        existing_shop_query = select(Shop).where(
            Shop.lattitude == shop_data.latitude,
            Shop.longitude == shop_data.longitude
        )
        existing_shop = session.exec(existing_shop_query).first()

        if existing_shop:
            raise HTTPException(
                status_code=409,
                detail="There is already a shop registered at these coordinates!!"
            )
        shop = Shop(
            name=shop_data.name,
            business_type=shop_data.business_type,
            lattitude=shop_data.latitude,
            longitude=shop_data.longitude,
            vendor_id=current_user.id
        )

        session.add(shop)
        session.commit()
        session.refresh(shop)

        return ShopResponse(
            id=shop.id,
            name=shop.name,
            business_type=shop.business_type,
            latitude=shop.lattitude,
            longitude=shop.longitude,
            vendor_name=current_user.name
        )


def get_shop_by_id(shop_id: str) -> ShopResponse:
    with Session(engine) as session:
        statement = select(Shop).join(User).where(Shop.id == shop_id)
        shop = session.exec(statement).first()
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")

        # Query to get the vendor name
        vendor_statement = select(User).where(User.id == shop.vendor_id)
        vendor = session.exec(vendor_statement).first()

        return ShopResponse(
            id=shop.id,
            name=shop.name,
            business_type=shop.business_type,
            latitude=shop.lattitude,
            longitude=shop.longitude,
            vendor_name=vendor.name if vendor else "Unknown"
        )


def get_shops_by_vendor(current_user: User = Depends(get_curr_user)) -> List[ShopResponse]:
    with Session(engine) as session:
        statement = select(Shop).where(Shop.vendor_id == current_user.id)
        shops = session.exec(statement).all()

        return [
            ShopResponse(
                id=shop.id,
                name=shop.name,
                business_type=shop.business_type,
                latitude=shop.lattitude,
                longitude=shop.longitude,
                vendor_name=current_user.name
            ) for shop in shops
        ]


def update_shop(shop_id: str, shop_update: ShopUpdate, current_user: User = Depends(get_curr_user)) -> ShopResponse:
    with Session(engine) as session:
        statement = select(Shop).where(Shop.id == shop_id,
                                       Shop.vendor_id == current_user.id)
        shop = session.exec(statement).first()

        if not shop:
            raise HTTPException(
                status_code=404, detail="Shop not found!!")

        if shop_update.name is not None:
            shop.name = shop_update.name
        if shop_update.business_type is not None:
            shop.business_type = shop_update.business_type
        if shop_update.latitude is not None:
            shop.lattitude = shop_update.latitude
        if shop_update.longitude is not None:
            shop.longitude = shop_update.longitude

        shop.updated_at = datetime.now(timezone.utc)

        session.add(shop)
        session.commit()
        session.refresh(shop)

        return ShopResponse(
            id=shop.id,
            name=shop.name,
            business_type=shop.business_type,
            latitude=shop.lattitude,
            longitude=shop.longitude,
            vendor_name=current_user.name
        )


def delete_shop(shop_id: str, current_user: User = Depends(get_curr_user)) -> dict:
    with Session(engine) as session:
        statement = select(Shop).where(Shop.id == shop_id,
                                       Shop.vendor_id == current_user.id)
        shop = session.exec(statement).first()

        if not shop:
            raise HTTPException(
                status_code=404, detail="Shop not found!!")

        session.delete(shop)
        session.commit()

        return {"detail": "Shop deleted successfully"}
