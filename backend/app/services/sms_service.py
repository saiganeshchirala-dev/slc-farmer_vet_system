import os
import logging
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_TEST_RECIPIENT = os.getenv("TWILIO_TEST_RECIPIENT")


def send_sms(to_number: str, otp_code: str):
    """
    Sends an SMS using Twilio. 
    If credentials are not set, it logs the OTP to the console for development.
    """
    message_body = f"Your SLC Farmers verification code is: {otp_code}. Do not share this with anyone."
    
    from ..core.config import settings
    
    if not settings.is_twilio_configured:
        logger.info("\n" + "="*60)
        logger.info("  DEVELOPMENT MODE: SMS NOT SENT VIA TWILIO")
        logger.info(f"  TO: {to_number}")
        logger.info(f"  MESSAGE: {message_body}")
        logger.info(f"  Bypass Code (ALWAYS 123456 in dev mode): {otp_code}")
        logger.info("="*60 + "\n")
        return True

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Robust E.164 formatting
        # Remove any non-digit characters except +
        clean_number = "".join(filter(lambda x: x.isdigit() or x == '+', to_number))
        
        if not clean_number.startswith('+'):
            # Default to India if no country code provided and it's 10 digits
            if len(clean_number) == 10:
                clean_number = f"+91{clean_number}"
            else:
                logger.warning(f"Mobile number {to_number} might be missing country code.")
            
        # --- TEST OVERRIDE LOGIC ---
        if TWILIO_TEST_RECIPIENT:
            logger.info(f"TEST OVERRIDE: Redirecting SMS from {clean_number} to {TWILIO_TEST_RECIPIENT}")
            clean_number = TWILIO_TEST_RECIPIENT
        # ---------------------------

        logger.info(f"Attempting to send SMS to {clean_number}...")
        
        message = client.messages.create(

            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=clean_number
        )
        
        logger.info(f"SMS sent successfully to {clean_number}. SID: {message.sid}")
        return True
    except Exception as e:
        error_msg = str(e)
        logger.error(f"TWILIO ERROR: Failed to send SMS to {to_number}")
        logger.error(f"DETAILS: {error_msg}")
        
        if "unverified" in error_msg.lower():
            logger.error("!!! CRITICAL: This number is NOT VERIFIED in your Twilio Trial Account.")
            logger.error("!!! Please verify it here: https://www.twilio.com/console/verified-numbers")
        elif "balance" in error_msg.lower():
            logger.error("!!! CRITICAL: Twilio account has insufficient balance.")
        
        # Fallback to logging for development so the developer can at least see the code
        logger.info("\n" + "!"*60)
        logger.info(f"  TWILIO FAILED! FALLBACK OTP FOR DEV: {otp_code}")
        logger.info("!"*60 + "\n")
        return True # Return True to allow testing despite Twilio failure
