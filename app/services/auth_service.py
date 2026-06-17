from app.auth.password_handler import DUMMY_HASH, verify_password, hash_password
def signup_user(email:str, password: str):
    hashed_password = hash_password(password)
    

