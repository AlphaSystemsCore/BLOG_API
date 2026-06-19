from app.auth.password_handler import DUMMY_HASH, verify_password, hash_password
from app.repositories.auth_repos import (
    get_email,
    create_user,)

class EmailExistsError(Exception):
    pass
class InvalidPasswordLenghtError(Exception):
    pass
import secrets
def gen_email_verification_token():
    # generation of token for email verification 
    return secrets.token_urlsafe(64)

def signup_user_service(email:str, password: str):
    # registers_user in the system
    try:
        if len(password) < 8:
            raise InvalidPasswordLenghtError("Password length must be greater than 7")
        
        hashed_password = hash_password(password)
        if get_email(email):
            raise EmailExistsError
        email_verification_token = gen_email_verification_token()
        hashed_emvt = hash_password(email_verification_token)
        
        create_user(email, hashed_password, hashed_emvt)
    except Exception as e:
        print("Error: ",e)
        raise 
    return email_verification_token
    

