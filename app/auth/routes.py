from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.auth import schemas, models, utils
from app.auth.schemas import ForgotPassword, ResetPassword
from app.auth.utils import hash_password, verify_password, generate_reset_token, send_reset_email
from datetime import datetime
from app.utils import oauth2
from app.auth.models import User, PasswordResetToken
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")
    
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully."}

@router.post("/signin")
def login(users_credentials: OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    user= db.query(User).filter(User.email == users_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Email")
    
    if not verify_password(users_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
    token_data = {"user_id": user.id, "role": user.role}
    return {
        "access_token": oauth2.create_access_token(token_data),
        "refresh_token": oauth2.create_refresh_token(token_data),
        "token_type": "bearer",
        "user": user.email
    }

@router.post("/forgot-password",status_code=status.HTTP_201_CREATED)
def secure_forgot_password(request: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    token, expires_at = generate_reset_token()
    reset_token = PasswordResetToken(token=token, user_id=user.id, expires_at=expires_at)
    db.add(reset_token)
    db.commit()
    
    return {"message": "Reset token created", "token": token}  


@router.post("/reset-password")
def secure_reset_password(request: ResetPassword, db: Session = Depends(get_db)):
    token_entry = db.query(PasswordResetToken).filter(PasswordResetToken.token == request.token).first()

    if not token_entry or token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    user = db.query(User).filter(User.id == token_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.hashed_password = hash_password(request.new_password)
    print(user.hashed_password)

    # Invalidate token after use
    db.delete(token_entry)
    db.commit()

    return {"message": "Password successfully reset"}