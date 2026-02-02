import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import models
from app.db.database import SQLALCHEMY_DATABASE_URL

def check_users():
    print("--- User Database Records ---")
    
    # Connect directly to the database
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        users = db.query(models.User).all()
        
        if not users:
            print("No users found in the database.")
            return

        print(f"Total Users: {len(users)}")
        print("-" * 50)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.full_name}")
            print(f"Mobile: {user.mobile_number}")
            print(f"Role: {user.role}")
            print(f"Village: {user.village}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
