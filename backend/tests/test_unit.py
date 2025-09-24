import pytest
from app.utils import hash_password, verify_password, create_access_token

# -------- Test password hashing and verification --------
def test_password_hashing():
    password = "mypassword"
    hashed = hash_password(password)
    
    # Correct password should verify
    assert verify_password(password, hashed) is True
    
    # Wrong password should fail
    assert verify_password("wrongpassword", hashed) is False

# -------- Test JWT token creation --------
def test_jwt_token():
    data = {"user_id": 1}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
