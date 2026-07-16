from psycopg2 import errors
import secrets
from datetime import datetime, timedelta, timezone

from app.auth.jwt_handler import (
    create_access_token, 
    create_refresh_token, 
    decode_refresh_token)
from app.auth.token_handler import hash_token
from app.auth.password_handler import hash_password, verify_password, DUMMY_HASH
from app.repositories.auth_repos import (
    register_user_save_evt, 
    consume_token_repo, 
    save_refresh_token_repo, 
    get_hashed_password_repo, 
    consume_refresh_token_repo, 
    create_new_email_verification_token_repo
)
from app.exceptions.auth_exception import (
    InvalidEmailVerificationTokenError, 
    EmailNotFoundError, 
    InvalidPasswordError, 
    RefreshTokenAlreadyConsumed, 
    FailedToCreateVerificationLinkError
)
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

class RegistrationError(Exception):
    pass

def register_user_service(username: str, email: str, password:str):
    """
    This service create user and send an email verification link to the user, to verify their gmail account
    This to avoid having invalid email and preventing typo email or impersonification using email
    evt is email_verification_token
    """
    hashed_password = hash_password(password)
    email_verification_token, hashed_evt, expire_at = create_email_verification_token_service()
    try:
        row = register_user_save_evt_repo(username, email, hashed_password, hashed_evt, expire_at)

        if row is None:
            raise RegistrationError("FAILED TO REGISTER USER, PLEASE TRY AGAIN")
        user_id = row.get("user_id")
        verification_link = email_formater_service(user_id, email_verification_token, email)
    except errors.UniqueViolation as e:
        print("Error: ", e)
        raise
    else:
        return verification_link
class EmailLookUpError(Exception):
    pass

def resend_email_verification_token(email: str):
    """
    Create new email_verification_token and send to the user
    Later ill add email background process to send link to users emails
    """
    email_verification_token, hashed_evt, expire_at = create_email_verification_token_service()

    user_id = create_new_email_verification_token_repo(email, hashed_evt, expire_at)
    if user_id is None:
        raise EmailLookUpError("FAILED CHECK YOU EMAIL AND TRY AGAIN")
    verification_link = email_formater_service(user_id, email_verification_token, email)
    return verification_link

def email_formater_service(user_id, email_verification_token, email):

    """ 
        email service to send email to be implemented later, now Im using JSON response to validate emails which is not
        even an inch secure.
    """
    link = "http://127.0.0.1:8000/auths/verify-email"
    path_params = f"{user_id}/{email_verification_token}"
    verification_link = f"{link}/{path_params}"
    return verification_link
class TokenExpiredError(Exception):
    pass
class InvalidUserIdError(Exception):
    pass

def verify_email_service(user_id: str, email_verification_token:str):
    """verifys emails from the link, and marks user as verified, guarantees email ownership"""
    hashed_email_verification_token = hash_token(email_verification_token)
    feedback = consume_token_repo(user_id, hashed_email_verification_token)
    if feedback == "expired":
        raise TokenExpiredError("EMAIL VERIFICATION TOKEN HAVE EXPIRED, KINDLY REQUEST FOR ANOTHER ONE")
    elif feedback == "invalid":
        raise InvalidEmailVerificationTokenError("INVALID EMAIL VERIFICATION TOKEN")
    elif feedback is None:
        raise InvalidUserIdError("THE USER_ID IS INCORRECT")
    else:
        user_id = feedback
    return "verified successfully"


def login_service(email:str, password: str, client:str):
    """Logs in the user using email and password"""
    row = get_hashed_password_repo(email)
    if row is None:
        verify_password(password, DUMMY_HASH)
        raise EmailNotFoundError("EMAIL NOT FOUND ERROR")
    user_id = row.get("user_id")
    hashed_password = row.get("hashed_password")
    if not verify_password(password, hashed_password):
        raise InvalidPasswordError("INVALID PASSWORD ERROR")
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
    """ all contained creating refresh token, hashing it, saving it and returning the signed token(jwt)"""
    refresh_token_value = gen_random_service()
    hashed_refresh_token_value = hash_token(refresh_token_value)
    expire_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE_TIME_DAYS)

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
    return refresh_token_jwt

def create_new_access_and_refresh_token_service(refresh_token_jwt: str, client:str):
    """creating new access and refresh tokens during refresh-when the access_token have expired"""
    user_id, jti, refresh_token_value = decode_refresh_token(refresh_token_jwt)
    """creating new access token """
    access_token = create_access_token_service(user_id)

    #hashing the refresh token to check it against the stored hash
    hashed_refresh_token_value = hash_token(refresh_token_value)
    verify_token_service(jti, refresh_token_value)
    refresh_token = create_refresh_token_service(user_id, client)
    return access_token, refresh_token

def verify_token_service(jti, hashed_refresh_token_value):
    """
    consumes and verifys the refresh token
    if the refresh_token is used then
    """
    if consume_refresh_token_repo(jti, hashed_refresh_token_value) is None:
        raise RefreshTokenAlreadyConsumed("TOKEN HAVE ALREADY BEEN USED")
    





