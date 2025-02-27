from pydantic import UUID4, EmailStr
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime, timezone
from typing import Optional, List


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    pass_hash: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    shops: List["Shop"] = Relationship(back_populates="vendor")


class UserCreate(SQLModel):
    name: str
    email: str
    password: str


class UserResponse(SQLModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime]


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserLogin(SQLModel):
    email: str
    password: str
