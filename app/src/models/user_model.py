from pydantic import UUID4, EmailStr
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
from typing import Optional, List
from src.models.shop_model import Shop


class User(SQLModel, table=True):
    id: UUID4 | None = Field(default=UUID4, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    pass_hash: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    shops: List["Shop"] = Relationship(back_populates="vendor")


class UserCreate(SQLModel):
    name: str
    email: str
    password: str


class UserResponse(SQLModel):
    id: UUID4
    name: str
    email: EmailStr
    created_at: datetime


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
