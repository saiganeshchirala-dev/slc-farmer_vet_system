from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .... import crud, schemas, db as database_module
from ....core import security
from ....services import sms_service

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/send-otp")
def send_otp(request: schemas.OTPRequest, db: Session = Depends(database_module.get_db)):
    # 1. Generate OTP
    otp_record = crud.create_otp(db, request.mobile_number)
    
    # 2. Send SMS via service
    sms_sent = sms_service.send_sms(request.mobile_number, otp_record.otp_code)
    
    if not sms_sent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to send SMS"
        )

    return {"message": "OTP sent successfully", "otp": otp_record.otp_code}

@router.post("/verify-otp")
def verify_otp(request: schemas.OTPVerify, db: Session = Depends(database_module.get_db)):
    is_valid = crud.verify_otp_db(db, request.mobile_number, request.otp)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
        
    user = crud.get_user_by_mobile(db, request.mobile_number)
    user_exists = True if user else False
    
    # Generate JWT Token
    access_token = security.create_access_token(subject=request.mobile_number)
    
    return {
        "message": "OTP verified successfully",
        "user_exists": user_exists,
        "mobile_number": request.mobile_number,
        "role": user.role if user else None,
        "access_token": access_token,
        "token_type": "bearer"
    }
