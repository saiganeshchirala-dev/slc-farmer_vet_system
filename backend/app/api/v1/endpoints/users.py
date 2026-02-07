from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .... import crud, schemas, db as database_module
from ....core import security

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/signup", response_model=schemas.UserAuthResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database_module.get_db)):
    db_user = crud.get_user_by_mobile(db, mobile_number=user.mobile_number)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this mobile number already registered")
    
    new_user = crud.create_user(db=db, user=user)
    
    # Generate Access Token
    access_token = security.create_access_token(subject=new_user.mobile_number)
    
    return {
        "message": "Registration successful",
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/{mobile_number}", response_model=schemas.User)
def read_user(mobile_number: str, db: Session = Depends(database_module.get_db)):
    db_user = crud.get_user_by_mobile(db, mobile_number=mobile_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
