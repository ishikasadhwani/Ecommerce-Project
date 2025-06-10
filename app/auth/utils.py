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

def send_reset_email(email: str, token: str):
    print(f"Send email to {email} with token: {token}")