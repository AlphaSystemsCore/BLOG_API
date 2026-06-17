from app.auth.password_handler import DUMMY_HASH, verify_password, hash_password
from app.repositories.auth_repos import get_email

class EmailExistsError(Exception):
    pass
class InvalidPasswordLenghtError(Exception):
    pass
import secrets
def gen_email_verification_token():
    # generation of token for email verification 
    return secrets.token_urlsafe(64)

def signup_user(email:str, password: str):
    # registers_user in the system
    if len(password) < 8:
        raise InvalidPasswordLenghtError("Password length must be greater than 7")
    
    hashed_password = hash_password(password)
    if get_email(email):
        raise EmailExistsError
    email_verification_token = gen_email_verification_token()
    hashed_emvt = hash_password(email_verification_token)
    try:
        
    return email_verification_token
    

    

if __name__ == "__main__":
    signup_user("darmaris@cheka.com", "kk")

