import hashlib

def hash_token(token):
    f_token = f"{token}"
    hash = hashlib.sha256(b'f_token').hexdigest()
    return hash


if __name__ == "__main__":
    if "c54cf50249ce810e32982ade16f47cd287bcff6c02141007ed535eaed00fba55" ==  hash_token("I'm runnig mad"):
        print("T")
    else:
        print("F")
   