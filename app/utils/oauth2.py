# Import necessary libraries and modules
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.auth.schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.models import User
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch secret key and algorithm from environment variable
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_EXPIRE_MIN = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

def create_access_token(data:dict):
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the token.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    """
    Verify a JWT access token and return token data.

    Args:
        token (str): JWT token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.

    Returns:
        TokenData: Token data containing user ID.

    Raises:
        HTTPException: If token is invalid or user_id is missing.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id = id)
        
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current authenticated user from the JWT token.

    Args:
        token (str): JWT token from the request.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid or user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()

    if not user:
        raise credentials_exception

    return user

def get_admin_user(user: User = Depends(get_current_user)):
    """
    Dependency to get an authenticated admin user.

    Args:
        user (User): The current authenticated user.

    Returns:
        User: The authenticated admin user object.

    Raises:
        HTTPException: If the user is not an admin.
    """
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user

def get_user_only(user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get a regular authenticated user (not admin).

    Args:
        user (User): The current authenticated user.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user is not a regular user.
    """
    if user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can access this functionality."
        )
    return user

def create_refresh_token(data: dict):
    """
    Create a JWT refresh token.

    Args:
        data (dict): Data to encode in the token.

    Returns:
        str: Encoded JWT refresh token.
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=REFRESH_EXPIRE_MIN)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Decode a JWT token and retrieve the associated user.

    Args:
        token (str): JWT token from the request.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The user associated with the token.

    Raises:
        HTTPException: If the token is invalid or user does not exist.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")