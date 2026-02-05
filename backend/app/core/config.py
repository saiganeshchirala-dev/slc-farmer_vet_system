import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Farmers Vet System"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv("TWILIO_PHONE_NUMBER")

    @property
    def is_twilio_configured(self) -> bool:
        return bool(
            self.TWILIO_ACCOUNT_SID and 
            self.TWILIO_AUTH_TOKEN and 
            self.TWILIO_PHONE_NUMBER and 
            "your_" not in self.TWILIO_ACCOUNT_SID.lower()
        )

    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://slcvet.com",
        "https://www.slcvet.com"
    ]

settings = Settings()
