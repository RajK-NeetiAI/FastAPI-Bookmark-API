import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


MONGODB_URL = os.getenv("MONGODB_URL")
JWT_SECRET = os.getenv("JWT_SECRET")


class Settings(BaseSettings):
    mongodb_url: str = MONGODB_URL
    database_name: str = "bookmarks_db"
    jwt_secret: str = JWT_SECRET
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


settings = Settings()
