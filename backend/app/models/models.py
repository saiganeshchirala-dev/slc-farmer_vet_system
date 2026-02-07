from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    mobile_number = Column(String, unique=True, index=True)
    role = Column(String) # farmer, vet, paravet
    dob = Column(String, nullable=True)
    state = Column(String)
    district = Column(String)
    mandal = Column(String, nullable=True)
    village = Column(String, nullable=True)
    language = Column(String, nullable=True)
    registration_num = Column(String, nullable=True) # Vet only
    degree = Column(String, nullable=True) # Vet only
    email = Column(String, nullable=True) # Vet only
    hospital_name = Column(String, nullable=True) # Vet only
    working_area = Column(String, nullable=True) # Vet/Paravet
    qualification = Column(String, nullable=True) # Legacy
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    animals = relationship("Animal", back_populates="owner")

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String) # Cattle, Buffalo, Sheep, Goat, etc.
    breed = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    tag_number = Column(String, unique=True, index=True, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="animals")
    
    created_at = Column(DateTime, default=datetime.utcnow)

class OTP(Base):
    __tablename__ = "otps"
    # ... (no changes to OTP)
    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String, index=True)
    otp_code = Column(String)
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)
