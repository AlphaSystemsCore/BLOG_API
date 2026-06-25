import hashlib

def hash_token(token):
    f_token = f"{token}"
    hash = hashlib.sha256(b'f_token').hexdigest()
    return hash

