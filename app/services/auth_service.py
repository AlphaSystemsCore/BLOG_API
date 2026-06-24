from psycopg2 import errors
import secrets
from datetime import datetime, timedelta, timezone

from app.auth.password_handler import hash_password, verify_password, DUMMY_HASH
from app.repositories.auth_repos import register_user_save_evt
EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES=15

def gen_random_service():
    return secrets.token_urlsafe()

def create_email_verification_token_service():
    email_verification_token =  gen_random_service()
    hashed_evt = hash_password(email_verification_token)
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES)
    return email_verification_token, hashed_evt, expire_at

def register_user_service(username: str, email: str, password:str):
    hashed_password = hash_password(password)
    email_verification_token, hashed_evt, expire_at = create_email_verification_token_service()
    try:
        user_id, token_id = register_user_save_evt(username, email, hashed_password, hashed_evt, expire_at)
        message = email_formater_service(user_id,token_id, email)
    except errors.UniqueViolation as e:
        print("Error: ", e)
        raise
    else:
        return message

def email_formater_service(user_id, token_id, email):
    # email to be implemented later, now I return JSON response with the token
    # to --email_formater_and_sender_service
    message = f"http://127.0.0.1:8000/auths/verify-email/{user_id}/{token_id}"
    return message
    
def verify_email_service(user_id: str, token_id:str):
    pass
