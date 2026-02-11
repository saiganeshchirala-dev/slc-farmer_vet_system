import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import models
from app.db.database import SQLALCHEMY_DATABASE_URL

def check_db():
    print("=" * 100)
    print("DATABASE INSPECTION TOOL (Enhanced)")
    print("=" * 100)
    
    # Connect directly to the database
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Ensure tables exist
    from app.db.database import Base
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check Users
        print("\n--- [ Table: users ] ---")
        users = db.query(models.User).all()
        if not users:
            print("No records found in 'users' table.")
        else:
            print(f"Total Records: {len(users)}")
            print("-" * 100)
            # Define header
            header = f"{'ID':<4} | {'Name':<15} | {'Mobile':<12} | {'Role':<8} | {'State':<12} | {'District':<12} | {'Village':<12}"
            print(header)
            print("-" * 100)
            for user in users:
                name = str(user.full_name)[:15]
                mobile = str(user.mobile_number)
                role = str(user.role)
                state = str(user.state)[:12]
                district = str(user.district)[:12]
                village = str(user.village)[:12]
                print(f"{user.id:<4} | {name:<15} | {mobile:<12} | {role:<8} | {state:<12} | {district:<12} | {village:<12}")
        
        # Check OTPs
        print("\n--- [ Table: otps ] ---")
        otps = db.query(models.OTP).all()
        if not otps:
            print("No records found in 'otps' table.")
        else:
            print(f"Total Records: {len(otps)}")
            print("-" * 100)
            header = f"{'ID':<4} | {'Mobile':<15} | {'OTP':<6} | {'Verified':<8}"
            print(header)
            print("-" * 100)
            for otp in otps:
                print(f"{otp.id:<4} | {str(otp.mobile_number):<15} | {str(otp.otp_code):<6} | {str(otp.is_verified):<8}")
        
        print("\n" + "=" * 100)
            
    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
