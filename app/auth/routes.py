from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.auth import schemas, models, utils
# from app.utils.jwt import create_token
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=201)
def signup(user: schemas.SignupSchema, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully."}