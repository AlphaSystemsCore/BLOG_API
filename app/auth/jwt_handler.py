import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from typing import Annotated
from datetime import datetime, timedelta, timezone

ACCESS_TOKEN_SECRET
REFRESH_TOKEN_SECRET
REFRESH_TOKEN_EXPIRY_DAYS
ACCESS_TOKEN_EXPIRY_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auths/login")


def create_access_token(data,  expiry_delta: timedelta | None = None):
    to_encode = data.copy()
    if expiry_delta:
        exp = datetime.now(timezone.utc) + expiry_delta
    else: 
        exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": exp})
    encoded = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # letter I will scale to be role based auth for endpoints
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if user_id == None:
            # ill add database check for lookup??
            raise HTTPException(
                status_code=401,
                detail="Not authorized"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = 401,
            detail = "Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code = 401,
            detail = "Token not valid"
        )
    else: 
        return user_id


def create_refresh_token(data: dict):
    to_encoded = data.copy()
    encoded = jwt.encode(to_encoded, REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded
  

def decode_refresh_token(token:str):
    CredentialError = HTTPException(
        status_code=401,
        detail="Not Authorized"
    )
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        user_id =payload.get("sub")
        jti = payload.get("jti")
        refresh_token =payload.get("refresh_token")
        if user_id is None and jti is None and refresh_token is None:
            raise CredentialError

        # will do db lookup for the user_id
    except jwt.exceptions.ExpiredSignatureError as e:
        raise CredentialError
    except jwt.exceptions.InvalidTokenError as e:
        raise CredentialError

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    else:
        return user_id, jti, refresh_token
    