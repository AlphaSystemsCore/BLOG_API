from datetime import datetime, timedelta, timezone

from app.auth.password_handler import DUMMY_HASH, verify_password, hash_password
from app.repositories.auth_repos import (
    get_email,
    register_user_repo,
    get_hashed_password_user_id_repo,
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
        
        register_user_repo(email, hashed_password, hashed_emvt, expire_at)
    except Exception as e:
        print("Error: ",e)
        raise 
    return email_verification_token
#to exceptions
class CredentialError(Exception):
    pass
  

def login_user_service(email: str, password: str):
    row = get_hashed_password_user_id_repo(email)
    if not row:
        hash_password(password, DUMMY_HASH)
        raise  CredentialError
    data = {
        "hashed_password": row[0],
        "user_id": row[1]
    }
    if not verify_password(password, data.get("hashed_password")):
        raise CredentialError
    

