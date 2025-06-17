# Import necessary modules and functions
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.auth import schemas, crud
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return crud.signup_user(user, db)

@router.post("/signin")
def login(users_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return JWT tokens.
    """
    return crud.login_user(users_credentials, db)

@router.post("/forgot-password", status_code=status.HTTP_201_CREATED)
def forgot_password(data: schemas.ForgotPassword, db: Session = Depends(get_db)):
    """
    Generate a secure password reset token and email it to the user.
    """
    return crud.forgot_password(data, db)

@router.post("/reset-password")
def secure_reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)):
    """
    Reset user password using a valid token.
    """
    return crud.reset_password(request, db)
