import pytest
from httpx import AsyncClient
from fastapi import status
from bson import ObjectId
from datetime import datetime, timezone

from src.models.schemas import BookmarkResponse


@pytest.fixture
async def test_bookmark(test_db, test_user):
    bookmark_data = {
        "_id": ObjectId(),
        "user_id": test_user["_id"],
        "title": "Test Bookmark",
        "url": "https://test.com",
        "description": "Test description",
        "created_at": datetime.now(tz=timezone.utc),
        "is_deleted": False
    }
    await test_db.bookmarks.insert_one(bookmark_data)
    return bookmark_data


async def test_create_bookmark(authenticated_client: AsyncClient):
    response = await authenticated_client.post(
        "/bookmarks/create",
        json={
            "title": "New Bookmark",
            "url": "https://example.com",
            "description": "Example description"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data: BookmarkResponse = await response.json()
    assert data.title == "New Bookmark"
    assert data.url == "https://example.com"
    assert not data.is_deleted


async def test_get_bookmarks(authenticated_client: AsyncClient, test_bookmark):
    response = await authenticated_client.get("/bookmarks/get")
    assert response.status_code == status.HTTP_200_OK
    data = await response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == test_bookmark["title"]


async def test_update_bookmark(authenticated_client: AsyncClient, test_bookmark):
    response = await authenticated_client.put(
        f"/bookmarks/update/{str(test_bookmark['_id'])}",
        json={
            "title": "Updated Title",
            "description": "Updated description"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = await response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"


async def test_delete_bookmark(authenticated_client: AsyncClient, test_bookmark):
    response = await authenticated_client.delete(
        f"/bookmarks/delete/{str(test_bookmark['_id'])}"
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify bookmark is soft deleted
    response = await authenticated_client.get("/bookmarks/")
    data = await response.json()
    assert len(data) == 0
