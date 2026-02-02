from sqlalchemy.orm import Session
from . import models, schemas
import random
from datetime import datetime, timedelta

# User CRUD
def get_user_by_mobile(db: Session, mobile_number: str):
    return db.query(models.User).filter(models.User.mobile_number == mobile_number).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        mobile_number=user.mobile_number,
        full_name=user.full_name,
        role=user.role,
        dob=user.dob,
        state=user.state,
        district=user.district,
        mandal=user.mandal,
        village=user.village,
        language=user.language,
        registration_num=user.registration_num,
        degree=user.degree,
        email=user.email,
        hospital_name=user.hospital_name,
        working_area=user.working_area,
        qualification=user.qualification
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# OTP CRUD
def create_otp(db: Session, mobile_number: str):
    from .core.config import settings
    if settings.is_twilio_configured:
        otp_code = str(random.randint(100000, 999999))
    else:
        otp_code = "123456" # Default OTP for testing
    
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # In a real app, you would verify if an active OTP already exists or invalidate old ones
    db_otp = models.OTP(mobile_number=mobile_number, otp_code=otp_code, expires_at=expires_at)
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    return db_otp

def verify_otp_db(db: Session, mobile_number: str, otp_code: str):
    # Sort by id desc to get latest
    otp_record = db.query(models.OTP).filter(
        models.OTP.mobile_number == mobile_number,
        models.OTP.otp_code == otp_code,
        models.OTP.is_verified == False
    ).order_by(models.OTP.id.desc()).first()
    
    if not otp_record:
        return False
        
    if otp_record.expires_at < datetime.utcnow():
        return False
        
    otp_record.is_verified = True
    db.commit()
    return True
