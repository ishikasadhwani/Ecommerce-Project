# import uuid
# from fastapi import APIRouter, HTTPException, status, Depends
# from sqlalchemy.orm import Session
# from app.auth import schemas, models, utils
# from app.auth.schemas import ForgotPassword, ResetPassword
# from app.auth.utils import hash_password, validate_password_strength, verify_password, generate_reset_token
# from datetime import datetime, timedelta
# from app.core.config import logger
# from app.utils import oauth2
# from app.auth.models import User, PasswordResetToken
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from app.core.database import get_db
# from app.utils.email import send_reset_email

# router = APIRouter(prefix="/auth", tags=["Authentication"])

# @router.post("/signup", status_code=status.HTTP_201_CREATED)
# def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
#     logger.info(f"Signup attempt for email: {user.email}")
#     existing_user = db.query(models.User).filter_by(email=user.email).first()
#     if existing_user:
#         logger.warning(f"Signup failed: Email already registered - {user.email}")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")
    
#     validate_password_strength(user.password)
#     hashed_pwd = utils.hash_password(user.password)
#     new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_pwd, role=user.role)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     logger.info(f"User created successfully: {user.email}")
#     return {"message": "User created successfully."}

# @router.post("/signin")
# def login(users_credentials: OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
#     logger.info(f"Login attempt for email: {users_credentials.username}")
#     user= db.query(User).filter(User.email == users_credentials.username).first()

#     if not user:
#         logger.warning(f"Login failed: Invalid Email - {users_credentials.username}")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Email")
    
#     if not verify_password(users_credentials.password, user.hashed_password):
#         logger.warning(f"Login failed: Invalid Password for email - {users_credentials.username}")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
#     token_data = {"user_id": user.id, "role": user.role}
#     logger.info(f"Login successful for email: {users_credentials.username}")
#     return {
#         "message": "Login Successful",
#         "access_token": oauth2.create_access_token(token_data),
#         "refresh_token": oauth2.create_refresh_token(token_data),
#         "token_type": "bearer",
#         "user": user.email
        
#     }



# @router.post("/forgot-password",status_code=status.HTTP_201_CREATED)
# def forgot_password(data: schemas.ForgotPassword, db: Session = Depends(get_db)):
#     logger.info(f"Forgot password requested for email: {data.email}")
#     user = db.query(User).filter_by(email=data.email).first()
#     if not user:
#         logger.warning(f"Forgot password failed: User not found - {data.email}")
#         raise HTTPException(status_code=404, detail="No user with this email found.")

#     reset_token = PasswordResetToken(
#         user_id=user.id,
#         token=str(uuid.uuid4()),
#         expires_at=datetime.utcnow() + timedelta(minutes=30)
#     )
#     db.add(reset_token)
#     db.commit()

#     #  Send actual email
#     send_reset_email(user.email, reset_token.token)
#     logger.info(f"Password reset token created for user_id={user.id}, email={user.email}")

#     return {"message": "Reset link has been sent to your email.",
#             "token": reset_token.token}

# @router.post("/reset-password")
# def secure_reset_password(request: ResetPassword, db: Session = Depends(get_db)):
#     logger.info(f"Password reset attempt with token: {request.token}")

#     token_entry = db.query(PasswordResetToken).filter(
#         PasswordResetToken.token == request.token,
#         PasswordResetToken.used == False  # Only allow unused
#     ).first()

#     if not token_entry:
#         logger.warning(f"Password reset failed: Invalid token")
#         raise HTTPException(status_code=400, detail="Invalid or expired token.")

#     if token_entry.expires_at < datetime.utcnow():
#         logger.warning(f"Token expired: {request.token}")
#         raise HTTPException(status_code=400, detail="Token has expired.")

#     user = db.query(User).filter(User.id == token_entry.user_id).first()
#     if not user:
#         logger.error(f"Password reset failed: User not found for token - {request.token}")
#         raise HTTPException(status_code=404, detail="User not found.")

#     validate_password_strength(request.new_password)

#     user.hashed_password = hash_password(request.new_password)
#     token_entry.used = True  # Mark token as used

#     db.commit()
#     logger.info(f"Password reset successful for user {user.email}")

#     return {"message": "Password successfully reset"}


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
