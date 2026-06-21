import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
SECRET_KEY_0 ="43d34b96c25e5cdddcfa4362134f580ee17d2004a2b21004c5dfca79e696bc25"
SECRET_KEY_1 = "08678f712780dfa5bb45e108ada6f698d2ec565390a3069c2884df5e39e001d9"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme_1 = OAuth2PasswordBearer(tokenUrl="auth/re")

def create_token(data: dict, expiry_delta: timedelta|None = None):
    to_encode = data.copy()
    if expiry_delta:
        exp = datetime.now(timezone.utc) + expiry_delta
    else: 
        exp = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": exp})
    encoded = jwt.encode(to_encode, SECRET_KEY_0, algorithm=ALGORITHM)
    return encoded

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY_1, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except Exception as e:
        #
        raise
    else: 
        return user_id

def create_refresh_token(data:dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp":exp})
    encoded = jwt.encode(to_encode, SECRET_KEY_1, algorithm=ALGORITHM)
    return encoded

def get_refresh_token(refresh_token: str = Depends())