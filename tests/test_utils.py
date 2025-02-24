from src.utils.security import verify_password, get_password_hash


def test_password_hashing():
    password = "testpass123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)


async def test_token_creation_and_validation(test_user):
    from src.utils.security import create_token, get_current_user

    # Create token
    token = create_token({"sub": str(test_user["_id"])})
    assert token

    # Validate token
    user = await get_current_user(token)
    assert user["_id"] == test_user["_id"]
    assert user["email"] == test_user["email"]
