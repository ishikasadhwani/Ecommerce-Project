# Import necessary modules and classes
import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.auth import models, schemas, utils
from app.utils.oauth2 import create_access_token, create_refresh_token
from app.utils.email import send_reset_email
from app.core.config import logger
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


def signup_user(user: schemas.UserSignup, db: Session) -> dict:
    """
    Create a new user after checking for duplicate email.
    """
    logger.info(f"Signup attempt for email: {user.email}")
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        logger.warning(f"Signup failed: Email already registered - {user.email}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")

    utils.validate_password_strength(user.password)
    hashed_pwd = utils.hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created successfully: {user.email}")

    return {"message": "User created successfully."}


def login_user(users_credentials: OAuth2PasswordRequestForm, db: Session) -> dict:
    """
    Validate login credentials and return JWT tokens.
    """
    logger.info(f"Login attempt for email: {users_credentials.username}")
    user = db.query(models.User).filter(models.User.email == users_credentials.username).first()

    if not user:
        logger.warning("Login failed: Invalid Email")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email")

    if not utils.verify_password(users_credentials.password, user.hashed_password):
        logger.warning("Login failed: Invalid Password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    token_data = {"user_id": user.id, "role": user.role}
    logger.info("Login successful")
    return {
        "message": "Login Successful",
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
        "user": user.email
    }


def forgot_password(data: schemas.ForgotPassword, db: Session) -> dict:
    """
    Generate a reset token and email it to the user.
    """
    logger.info(f"Forgot password requested for email: {data.email}")
    user = db.query(models.User).filter_by(email=data.email).first()

    if not user:
        logger.warning("Forgot password failed: User not found")
        raise HTTPException(status_code=404, detail="No user with this email found.")

    reset_token = models.PasswordResetToken(
        user_id=user.id,
        token=str(uuid.uuid4()),
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(reset_token)
    db.commit()

    send_reset_email(user.email, reset_token.token)
    logger.info("Password reset token created")

    return {
        "message": "Reset link has been sent to your email.",
        "token": reset_token.token
    }


def reset_password(request: schemas.ResetPassword, db: Session) -> dict:
    """
    Reset the user password after validating token.
    """
    logger.info("Password reset attempt")

    token_entry = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == request.token,
        models.PasswordResetToken.used == False
    ).first()

    if not token_entry:
        logger.warning("Invalid or expired token")
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    if token_entry.expires_at < datetime.utcnow():
        logger.warning("Token expired")
        raise HTTPException(status_code=400, detail="Token has expired.")

    user = db.query(models.User).filter(models.User.id == token_entry.user_id).first()

    if not user:
        logger.error("User not found for token")
        raise HTTPException(status_code=404, detail="User not found.")

    utils.validate_password_strength(request.new_password)
    user.hashed_password = utils.hash_password(request.new_password)
    token_entry.used = True

    db.commit()
    logger.info(f"Password reset successful for user {user.email}")

    return {"message": "Password successfully reset"}
