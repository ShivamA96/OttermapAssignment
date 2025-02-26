from pydantic import UUID4, EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import uuid
from datetime import datetime
from typing import Optional, List

from app.src.models.user_model import User


class Shop(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    business_type: Optional[str] = None
    lattitude: float = Field()
    longitude: float = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    vendor_id: UUID4 = Field(foreign_key="user.id")

    vendor: User = Relationship(back_populates="shops")

# input validation


class ShopCreate(SQLModel):
    name: str
    business_type: str
    latitude: float
    longitude: float

# response validation


class ShopResponse(SQLModel):
    id: UUID4
    name: str
    business_type: str
    latitude: float
    longitude: float
    created_at: datetime
    vendor_id: UUID4

# update validation


class ShopUpdate(SQLModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# nearby query input validation


class NearbyShopQuery(SQLModel):
    """Schema for querying nearby shops."""
    latitude: float
    longitude: float
    radius: float = 5.0  # Default radius in kilometers
    limit: int = 10  # Default number of results to return
