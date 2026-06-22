from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
auth_router = APIRouter(tags=["Auths"])

from app.services.auth_service import EmailExistsError, InvalidPasswordLenghtError
from app.services.auth_service import register_user_service


@auth_router.post("/auth/register")
async def register_user(email:EmailStr= Form(), password: str = Form()):
    try:
        register_user_service(email, password)
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


@auth_router.get("/auth/verify-email/{email-verification-token}")
async def verify_user_email(email_verification_token: str):
    pass

@auth_router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass

@auth_router.get("/auth/refresh-access-token")
async def refresh_token():
    pass