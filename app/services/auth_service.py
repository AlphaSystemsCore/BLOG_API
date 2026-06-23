import psycopg2.errors
import secrets

from app.auth.password_handler import hash_password, verify_password, DUMMY_HASH
from app.repositories.auth_repos import register_user_save_evt
EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES=15
def gen_random_service():
    return secrets.token_urlsafe()

def create_email_verification_token_service():
    email_verification_token =  gen_random()
    hashed_evt = hash_password(email_verification_token)
    return email_verification_token, hashed_evt

def register_user_service(username: str, email: str, password:str):
    hashed_password = hash_password(password)
    email_verification_token, hashed_evt = create_email_verification_token()
    try:
        register_user_save_evt(username, email, hashed_password, hashed_evt, expire_at)
    except Exception as e:
        print(e)
        raise
    else:
        return email_verification_token

        

    
