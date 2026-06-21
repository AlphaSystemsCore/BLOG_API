import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from typing import Annotated
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_SECRET="43d34b96c25e5cdddcfa4362134f580ee17d2004a2b21004c5dfca79e696bc25"
REFRESH_TOKEN_SECRET = "08678f712780dfa5bb45e108ada6f698d2ec565390a3069c2884df5e39e001d9"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(sub:str,  expiry_delta: timedelta | None = None):
    to_encode = {
        "sub": sub,
        "type":"access_token"
    }
    if expiry_delta:
        exp = datetime.now(timezone.utc) + expiry_delta
    else: 
        exp = datetime.now(timezone.utc) + timedelta(minutes=20)
    to_encode.update({"exp": exp})
    encoded = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded

def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
    
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        if payload.get('type') == "access_token":
            user_id = payload.get("sub")
            if user_id == None:
                raise HTTPException(
                    status_code=401,
                    detail="Not authorized"
                )
        else: 
            raise HTTPException(
                status_code = 401,
                detail = "Not Authorized"
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
    except HTTPException:
        raise 
    else: 
        return user_id

def create_refresh_token(sub: str, jti: str):
    to_encode = {
        "sub": sub,
        "jti": jti,
        "type": "refresh_token"
    }
    exp = datetime.now(timezone.utc) + timedelta(days=20)
    to_encode.update({"exp":exp})
    encoded = jwt.encode(to_encode, REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded

def decode_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        if payload.get('type') == 'refresh_token':
            user_id = payload.get("sub")
            jti = payload.get("jti")
            if user_id == None and jti == None:
                raise HTTPException(
                    status_code=401,
                    detail="Not authorized"
                )
        else: 
            raise HTTPException(
                status_code = 401,
                detail = "Not Authorized"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code = 401,
            detail = "Token not valid"
        )
    except HTTPException:
        raise 
    else:
        return user_id, jti

