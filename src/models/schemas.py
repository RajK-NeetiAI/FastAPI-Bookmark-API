from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserInDb(BaseModel):
    id: str
    email: str
    username: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class BookmarkCreate(BaseModel):
    title: str
    url: str
    description: Optional[str] = None


class BookmarkUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class BookmarkResponse(BaseModel):
    id: str
    title: str
    url: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
