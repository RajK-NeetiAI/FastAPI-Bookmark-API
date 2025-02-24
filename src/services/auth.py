from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status

from src.database import db
from src.models.schemas import UserCreate, UserResponse, TokenResponse
from src.utils.security import get_password_hash, verify_password, create_token
from src.config import settings


async def create_user(user: UserCreate) -> UserResponse:
    # Check if user exists
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    user_dict["created_at"] = datetime.now(tz=timezone.utc)

    result = await db.users.insert_one(user_dict)

    created_user = await db.users.find_one({"_id": result.inserted_id})
    return UserResponse(
        id=str(created_user["_id"]),
        email=created_user["email"],
        username=created_user["username"],
        created_at=created_user["created_at"]
    )


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None
    return user


async def create_tokens(user_id: str) -> TokenResponse:
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)

    access_token = create_token(
        data={"sub": user_id},
        expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": user_id},
        expires_delta=refresh_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
