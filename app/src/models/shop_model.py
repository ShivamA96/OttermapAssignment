from pydantic import UUID4, EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import uuid
from datetime import datetime, timezone
from typing import Optional, List


class Shop(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    business_type: Optional[str] = None
    lattitude: float = Field()
    longitude: float = Field()
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    vendor_id: str = Field(foreign_key="user.id")

    vendor: "User" = Relationship(back_populates="shops")

# input validation


class ShopCreate(SQLModel):
    name: str
    business_type: str
    latitude: float
    longitude: float

# response validation


class ShopResponse(SQLModel):
    id: str
    name: str
    business_type: str
    latitude: float
    longitude: float
    vendor_name: str

# update validation


class ShopUpdate(SQLModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# nearby query input validation


class NearbyShopQuery(SQLModel):
    """Schema for querying nearby shops."""
    lattitude: float
    longitude: float
    radius: float = 5.0  # in km
    limit: int = 10
