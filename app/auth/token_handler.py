import hashlib


def hash_token(token):
    """hashes the tokens and provides the output as a hashed_value"""
    f_token = f"{token}"
    hashed_value = hashlib.sha256(f_token.encode()).hexdigest()
    return hashed_value

# if __name__ == "__main__":
#     answer = hash_token("alphonc") == hash_token("elvis")
#     print(answer)