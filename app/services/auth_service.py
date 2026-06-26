from psycopg2 import errors
import secrets
from datetime import datetime, timedelta, timezone

from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.auth.token_handler import hash_token
from app.auth.password_handler import hash_password, verify_password, DUMMY_HASH
from app.repositories.auth_repos import register_user_save_evt, consume_token_repo, save_refresh_token_repo, get_hashed_password_repo
from app.exceptions.auth_exception import InvalidEmailVerificationTokenError, EmailNotFoundError, InvalidPasswordError
EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES=15
TOKEN_BYTE_SIZE=32
ACCESS_TOKEN_VALID_TIME_MINUTES=15
REFRESH_EXPIRE_TIME_DAYS=30

def gen_random_service():
    return secrets.token_urlsafe(TOKEN_BYTE_SIZE)

def create_email_verification_token_service():
    email_verification_token =  gen_random_service()
    hashed_evt = hash_token(email_verification_token)
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES)
    return email_verification_token, hashed_evt, expire_at

def register_user_service(username: str, email: str, password:str):
    hashed_password = hash_password(password)
    email_verification_token, hashed_evt, expire_at = create_email_verification_token_service()
    try:
        user_id= register_user_save_evt(username, email, hashed_password, hashed_evt, expire_at)
        message = email_formater_service(user_id, email_verification_token, email)
    except errors.UniqueViolation as e:
        print("Error: ", e)
        raise
    else:
        return message

def email_formater_service(user_id, email_verification_token, email):
    # email to be implemented later, now I return JSON response with the token
    # to --email_formater_and_sender_service
    message = f"http://127.0.0.1:8000/auths/verify-email/{user_id}/{email_verification_token}"
    return message
    
def verify_email_service(user_id: str, email_verification_token:str):
    hashed_email_verification_token = hash_token(email_verification_token)
    row = consume_token_repo(user_id, hashed_email_verification_token)
    if not row:
        print(row)
        raise InvalidEmailVerificationTokenError
    print(row)
    return "verified successfully"


def login_service(email:str, password: str, client:str):
    row = get_hashed_password_repo(email)
    if not row:
        verify_password(password, DUMMY_HASH)
        raise EmailNotFoundError
    user_id = row[1]
    hashed_password = row[0]
    if not verify_password(password, hashed_password):
        raise InvalidPasswordError
    refresh_token_jwt = create_refresh_token_service(user_id, client)
    access_token_jwt = create_access_token_service(user_id)
    return refresh_token_jwt, access_token_jwt

def create_access_token_service(user_id: str):
    # creating access token and returning the signed token
    payload = {
        "sub": user_id,
    }
    access_token = create_access_token(payload)
    return access_token

def create_refresh_token_service(user_id: str, client:str):
    # all contained creating refresh token, hashing it, saving it and returning the signed token
    refresh_token_value = gen_random_service()
    hashed_refresh_token_value = hash_token(refresh_token_value)
    expire_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_TIME_DAYS)
    try:
        row = save_refresh_token_repo(user_id, hashed_refresh_token_value, client, expire_at)
        if row:
            jti = row[0]
        payload = {
        "sub": user_id,
        "refresh_token": refresh_token_value,
        "jti": jti,
        "exp": expire_at
        }
        refresh_token_jwt = create_refresh_token(payload)
    except Exception as exc:
        print(exc)
        raise 
    else:
        return refresh_token_jwt

if __name__ == "__main__":
    jwt = create_access_token_service("0e103f2c-4c8e-490e-88fa-4dda1e429800")
    print(jwt)

def unpack_refresh_token_jwt(refresh_token_jwt: str, client:str):
    user_id, jti, refresh_token_value = decode_refresh_token(refresh_token_jwt)
    print(user_id)
    
    