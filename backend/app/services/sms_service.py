import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_otp() -> str:
    """Generate a random 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_sms(to_number: str, otp_code: str) -> bool:
    """
    Simulates sending an SMS. 
    In production, you can integrate any SMS provider here.
    For now, it logs the OTP to the console.
    """
    message_body = f"Your SLC Farmers verification code is: {otp_code}. Do not share this with anyone."
    
    logger.info("\n" + "="*60)
    logger.info("  OTP GENERATED (No SMS Provider)")
    logger.info(f"  TO: {to_number}")
    logger.info(f"  OTP CODE: {otp_code}")
    logger.info(f"  MESSAGE: {message_body}")
    logger.info("="*60 + "\n")
    
    return True
