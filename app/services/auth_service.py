from psycopg2 import errors
import secrets
from datetime import datetime, timedelta, timezone

from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_refresh_token
from app.auth.token_handler import hash_token
from app.auth.password_handler import hash_password, verify_password, DUMMY_HASH
from app.repositories.auth_repos import register_user_save_evt, consume_token_repo, save_refresh_token_repo, get_hashed_password_repo, consume_refresh_token_repo
from app.exceptions.auth_exception import InvalidEmailVerificationTokenError, EmailNotFoundError, InvalidPasswordError, RefreshTokenAlreadyConsumed
# disclaimer
# to be moved to .env file this is just for demo
from app.core.load_envs import EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES, TOKEN_BYTE_SIZE, ACCESS_TOKEN_EXPIRY_MINUTES, REFRESH_EXPIRE_TIME_DAYS

def gen_random_service():
    """generating random value"""
    return secrets.token_urlsafe(TOKEN_BYTE_SIZE)

def create_email_verification_token_service():
    """creating email verification token, return the hashed_evt, evt, and expire at: evt-email_verification_token"""
    email_verification_token =  gen_random_service()
    hashed_evt = hash_token(email_verification_token)
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRES_MINUTES)
    return email_verification_token, hashed_evt, expire_at

def register_user_service(username: str, email: str, password:str):
    """this service create user and send an email verification link to the user, to verify their gmail account
    This to avoid having invalid email and preventing typo email or impersonification using email"""
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
    """ email service to send email to be implemented later, now Im using JSON response to validate emails which is not
    even an inch secure.
    """
    verification_link = f"http://127.0.0.1:8000/auths/verify-email/{user_id}/{email_verification_token}"
    return verification_link
    
def verify_email_service(user_id: str, email_verification_token:str):
    """verifys emails using an atomic transaction"""
    hashed_email_verification_token = hash_token(email_verification_token)
    row = consume_token_repo(user_id, hashed_email_verification_token)
    if not row:
        print(row)
        raise InvalidEmailVerificationTokenError
    print(row)
    return "verified successfully"


def login_service(email:str, password: str, client:str):
    """Logs in the user using email and password"""
    row = get_hashed_password_repo(email)
    if not row:
        verify_password(password, DUMMY_HASH)
        raise EmailNotFoundError
    user_id = row.get("user_id")
    hashed_password = row.get("hashed_password")
    if not verify_password(password, hashed_password):
        raise InvalidPasswordError
    refresh_token_jwt = create_refresh_token_service(user_id, client)
    access_token_jwt = create_access_token_service(user_id)
    return refresh_token_jwt, access_token_jwt

def create_access_token_service(user_id: str):
    """creating access token and returning the signed token"""
    payload = {
        "sub": user_id,
    }
    access_token = create_access_token(payload)
    return access_token

def create_refresh_token_service(user_id: str, client:str):
    """ all contained creating refresh token, hashing it, saving it and returning the signed token"""
    refresh_token_value = gen_random_service()
    hashed_refresh_token_value = hash_token(refresh_token_value)
    expire_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_TIME_DAYS)
    try:
        row = save_refresh_token_repo(user_id, hashed_refresh_token_value, client, expire_at)
        if row:
            jti = row.get("refresh_token_id")
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

def create_new_access_and_refresh_token_service(refresh_token_jwt: str, client:str):
    """creating new access and refresh tokens during refresh"""
    user_id, jti, refresh_token_value = decode_refresh_token(refresh_token_jwt)
    """creating new access token """
    access_token = create_access_token_service(user_id)

    hashed_refresh_token_value = hash_token(refresh_token_value)
    verify_token_service(jti, refresh_token_value)
    refresh_token = create_refresh_token_service(user_id, client)
    print(access_token)
    print(refresh_token)
    return access_token, refresh_token

def verify_token_service(jti, refresh_token_value):
    """consumes and verifys the refresh token"""
    hashed_refresh_token_value = hash_token(refresh_token_value)
    if not consume_refresh_token_repo(jti, hashed_refresh_token_value):
        raise RefreshTokenAlreadyConsumed
    



