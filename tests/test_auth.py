from httpx import AsyncClient
from fastapi import status


async def test_register_user(test_client: AsyncClient):
    response = await test_client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "newpass123",
            "username": "newuser"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = await response.json()
    assert "id" in data
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"


async def test_register_existing_user(test_client: AsyncClient, test_user):
    response = await test_client.post(
        "/auth/register",
        json={
            "email": test_user["email"],
            "password": "somepass123",
            "username": "someuser"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_login_success(test_client: AsyncClient, test_user):
    response = await test_client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": "testpass123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = await response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(test_client: AsyncClient, test_user):
    response = await test_client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": "wrongpass"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
