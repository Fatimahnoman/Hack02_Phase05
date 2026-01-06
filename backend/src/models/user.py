from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(UserBase):
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime