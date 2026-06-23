from datetime import datetime, timedelta, timezone

from app.auth.password_handler import DUMMY_HASH, verify_password, hash_password
from app.repositories.auth_repos import *
    
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app.exceptions.auth_exception import *


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
        # creating email verification token
        # emvt means email verification token
        email_verification_token = gen_email_verification_token()
        hashed_emvt = hash_password(email_verification_token)
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        
        user_id = register_user_repo(email, hashed_password, hashed_emvt, expire_at)
        if user_id is None:
            raise ValueError
    except Exception as e:
        print(e)
        raise
    else:
        return email_verification_token, user_id


def login_user_service(email: str, password: str, client: str):
    try:
        row = get_hashed_password_user_id_repo(email)
        if not row:
            verify_password(password, DUMMY_HASH)
            raise  CredentialError()
        if not row[2]:
            raise EmailNotVerifiedError()
    
        hashed_password= row[0]
        user_id =row[1]
        if not verify_password(password, hashed_password):
            raise CredentialError()

        # creating access_oken
        access_token =  create_access_token(user_id)
        # creating refresh_token

        refresh_token_value = gen_refresh_token()
        hashed_refresh_token = hash_password(refresh_token_value)
        refresh_token = create_refresh_token_service(user_id, hashed_refresh_token, client, expiry_at=datetime.now(timezone.utc)+timedelta(days=100))
        refresh_token.update({
            "sub": user_id,
            "token": refresh_token_value,
            "type": "refresh_token",
        })
        encoded_refresh_token = create_refresh_token(refresh_token)

    except CredentialError:
        raise
    else:
        return access_token, encoded_refresh_token



def create_refresh_token_service(user_id: str, hashed_refresh_token: str, client: str, expiry_at: datetime):
    # creating refresh token service to seperated from login for sepereration of con
    refresh_token_id = save_refresh_token(user_id, hashed_refresh_token, client, expiry_at)
    refresh_token = {
        "jti": refresh_token_id[0],
        "exp": expiry_at
    }
    return refresh_token
    

def validate_email_verification_service(user_id: str, email_verification_token: str):
    row = get_email_verification_metadate_repo(user_id)
    if not row:
        raise EmailVerificationTokenNotFoundError()
    data= {
        "hashed_email_verificaton_token": row[0],
        "is_used": row[1],
        "expire_at": row[2],
        "is_verified": row[3]
    }
    if data.get("expire_at") < datetime.now(timezone.utc):
        is_used = True
        update_email_verification_repo(user_id, is_used, datetime.now(timezone.utc))
        raise  EmailVerificationTokenExpired()
    if  data['is_used']  or  data['is_verified']:
        raise EmailVerificationTokenInvalidError()
    is_used = True
    is_verified =  True
    try:
        update_email_verification_repo(user_id, is_used, datetime.now(timezone.utc), is_verified)
    except Exception:
        raise
    
    
def refresh_access_token_service(user_id, jti, refresh_token, client):
    class RefreshTokenExpiredError(Exception):
        pass
    class InvalidRefreshToken(Exception):
        pass
    class RefreshTokenNotFoundError(Exception):
        pass
    row = get_refresh_token_metadata(jti)
    if row is None:
        raise  RefreshTokenNotFoundError()
    hashed_refresh_token = row[0]
    is_revoked = row[1]
    expiry_at = row[2]

    if expiry_at < datetime.now(timezone.utc):
        raise RefreshTokenExpiredError()
    if is_revoked or not verify_password(refresh_token, hashed_refresh_token):
        raise InvalidRefreshToken()


    new_refresh_token = gen_refresh_token()
    hashed_new_refresh_token = hash_password(new_refresh_token)
    # creating new refresh token 
    new_refresh_token = create_refresh_token_service(user_id, hashed_new_refresh_token, client, expiry_at=datetime.now(timezone.utc))
    # creating new refresh token 
    new_refresh_token.update({
        "sub":user_id,
        "type": "refresh_token",
        "token":new_refresh_token
    })
    update_refresh_token(jti)
    refresh_token = create_refresh_token(new_refresh_token)
    access_token = create_access_token(user_id)
   
    return access_token, refresh_token


    
    
    

    
