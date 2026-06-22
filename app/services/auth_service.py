from datetime import datetime, timedelta, timezone

from app.auth.password_handler import DUMMY_HASH, verify_password, hash_password
from app.repositories.auth_repos import (
    get_email,
    register_user_repo,
    get_hashed_password_user_id_repo,
    save_refresh_token
    )
from app.auth.jwt_handler import create_access_token, create_refresh_token

class EmailExistsError(Exception):
    pass
class InvalidPasswordLenghtError(Exception):
    pass

import secrets
def gen_email_verification_token():
    # generation of token for email verification 
    return secrets.token_urlsafe(64)

def gen_refresh_token():
    return secrets.token_urlsafe(32)

def register_user_service(email:str, password: str):
    # registers_user in the system
    # emvt is email_verification_token
    try:
        if len(password) < 8:
            raise InvalidPasswordLenghtError("Password length must be greater than 7")
        
        hashed_password = hash_password(password)
        if get_email(email):
            raise EmailExistsError
        email_verification_token = gen_email_verification_token()
        hashed_emvt = hash_password(email_verification_token)
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        
        user_id = register_user_repo(email, hashed_password, hashed_emvt, expire_at)
        if user_id is None:
            raise ValueError
    except Exception as e:
        raise
    else:
        return email_verification_token, user_id

#>>>>to exceptions
class CredentialError(Exception):
    pass
  

def login_user_service(email: str, password: str, client: str):
    try:
        row = get_hashed_password_user_id_repo(email)
        if not row:
            hash_password(password, DUMMY_HASH)
            raise  CredentialError()
    
        hashed_password= row[0]
        user_id =row[1]

        if not verify_password(password, hashed_password):
            raise CredentialError()
        # creating access_oken
        access_token =  create_access_token(user_id)
        # creating refresh_token
        refresh_token_value = gen_refresh_token()
        hashed_refresh_token = hash_password(refresh_token_value)
        refresh_token = create_refresh_token_service(user_id, hashed_refresh_token, client, expire_at=datetime.now(timezone.utc) + timedelta(days=30))
    except CredentialError:
        raise
    else:
        return access_token, refresh_token, refresh_token_value


def create_refresh_token_service(user_id: str, hashed_refresh_token: str, client: str, expire_at: datetime):
    refresh_token_id = save_refresh_token(user_id, hashed_refresh_token, client, expire_at)
    refresh_token = create_refresh_token(sub=user_id, jti=refresh_token_id, expire_at=expire_at)
    return refresh_token

def validate_email_token(user_id: str, email_verification_token: str):
    pass
    
