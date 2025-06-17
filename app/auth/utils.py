from fastapi import HTTPException, status
import re
from passlib.context import CryptContext
import uuid
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_reset_token(expiry_minutes=15):
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    return token, expires_at

def validate_password_strength(password: str):
    """
    Validates the strength of a password.
    Raises HTTPException with 400 if password is weak.
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must include at least one uppercase letter."
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must include at least one lowercase letter."
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must include at least one digit."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must include at least one special character."
        )


