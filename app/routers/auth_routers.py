from fastapi import Depends, APIRouter, HTTPException, status
from psycopg2 import errors

from app.schemas.auth_schemas import RegisterUser
from app.services.auth_service import register_user_service
auth_router = APIRouter(tags=["Auths"])


@auth_router.post("/auths/register")
def register_user(user: RegisterUser):
    try:
        email_verification_token = register_user_service(user.user_name, user.email, user.password)
    except errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already exist in the system"
        ) 
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "INTERNAL_SERVER_ERROR"
        )
    else:
        return email_verification_token

@auth_router.get("/auths/verify-email-account")
def verify_email(user_id: str, email_verification_token: str):
    pass