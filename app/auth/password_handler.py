from pwdlib import PasswordHash

DUMMY_PASSWD = 
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash(DUMMY_PASSWD) # to be taken in .env file

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

