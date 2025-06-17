# Import necessary modules and classes
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from enum import Enum

# Schema for user roles
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

# Schema for user signup
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum

    
    @validator("name")
    def not_empty(cls, v ):
        if v.strip()=="":
            raise ValueError("Name cannot be empty")
        return v

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for api response
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True

# Schema for token generation
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for decode token data
class TokenData(BaseModel):
    id: Optional[int]=None

# Schema for forgot password
class ForgotPassword(BaseModel):
    email: EmailStr

# Schema for reset password
class ResetPassword(BaseModel):
    token: str
    new_password: str 

    