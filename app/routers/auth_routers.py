from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
auth_router = APIRouter(tags=["Auths"])

from app.services.auth_service import EmailExistsError, InvalidPasswordLenghtError
from app.services.auth_service import register_user_service
from app.schemas.auth_schemas import RegisterUser


@auth_router.post("/auth/register")
async def register_user(user: RegisterUser):
    try:
        email_verification_token, user_id = register_user_service(user.email, user.password)
    except InvalidPasswordLenghtError as e:
        raise HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail=str(e)
        )
    except EmailExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='INTERNAL SERVER ERROR'
        )
    else:
        return{
            "msg": "verification link have been sent to your email kindly click the link to be logged in..."
        }


@auth_router.get("/auth/verify-email/{user_id}/{email-verification-token}")
async def verify_user_email(email_verification_token: str):
    pass

@auth_router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass

@auth_router.get("/auth/refresh-access-token")
async def refresh_token():
    pass