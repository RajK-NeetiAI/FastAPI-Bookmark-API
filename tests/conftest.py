import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator, Generator, Dict, Any
from bson import ObjectId

from src.main import app
from src.config import settings
from src.database import db
from src.utils.security import get_password_hash, create_token
from src import config

# Test database settings
TEST_MONGODB_URL = config.MONGODB_URL
TEST_DB_NAME = "test_bookmarks_db"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_client() -> AsyncGenerator:
    # Connect to test database
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    db = client[TEST_DB_NAME]

    # Override the database in the app
    app.state.db = db

    # Create test client
    with TestClient(app) as test_client:
        yield test_client

    # Cleanup - drop test database
    await client.drop_database(TEST_DB_NAME)
    client.close()


@pytest.fixture(scope="function")
async def test_db():
    # Connect to test database
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    db = client[TEST_DB_NAME]

    yield db

    # Cleanup after each test
    await client.drop_database(TEST_DB_NAME)
    client.close()


@pytest.fixture
async def test_user(test_db) -> Dict[str, Any]:
    user_data = {
        "_id": ObjectId(),
        "email": "test@example.com",
        "username": "testuser",
        "password": get_password_hash("testpass123"),
        "created_at": datetime.now(tz=timezone.utc)
    }
    await test_db.users.insert_one(user_data)
    return user_data


@pytest.fixture
def test_user_token(test_user: Dict[str, Any]) -> str:
    return create_token({"sub": str(test_user["_id"])})


@pytest.fixture
async def authenticated_client(test_client: TestClient, test_user_token: str) -> TestClient:
    test_client.headers = {
        **test_client.headers,
        "Authorization": f"Bearer {test_user_token}"
    }
    return test_client
