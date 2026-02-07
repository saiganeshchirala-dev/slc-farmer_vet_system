from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    mobile_number: str

class UserCreate(UserBase):
    full_name: str
    role: str
    dob: Optional[str] = None
    state: str
    district: str
    mandal: Optional[str] = None
    village: Optional[str] = None
    language: Optional[str] = None
    registration_num: Optional[str] = None
    degree: Optional[str] = None
    email: Optional[str] = None
    hospital_name: Optional[str] = None
    working_area: Optional[str] = None
    qualification: Optional[str] = None

class User(UserBase):
    id: int
    full_name: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OTPRequest(BaseModel):
    mobile_number: str

class OTPVerify(BaseModel):
    mobile_number: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserAuthResponse(BaseModel):
    message: str
    user: User
    access_token: str
    token_type: str
