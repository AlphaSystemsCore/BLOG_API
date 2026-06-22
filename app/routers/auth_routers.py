from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
auth_router = APIRouter(tags=["Auths"])


from app.services.auth_service import register_user_service, validate_email_verification_service
from app.schemas.auth_schemas import RegisterUser
from app.exceptions.auth_exception import *

@auth_router.post("/auth/register")
async def register_user(user: RegisterUser):
    try:
        email_verification_token, user_id = register_user_service(user.email, user.password)
        link = f"http://127.0.0.1:8000/auth/verify-email/{user_id}/{email_verification_token}"
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
    # except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='INTERNAL SERVER ERROR'
        )
       
    else:
        return{
            "msg": "verification link have been sent to your email kindly click the link to be logged in...",
            "link": link
        }


@auth_router.get("/auth/verify-email/{user_id}/{email_verification_token}")
async def verify_user_email(user_id:str, email_verification_token: str):
    validate_email_verification_service(user_id, email_verification_token)
    return {
        "msg":"email verified successfully, proceed to login"
    }

@auth_router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass

@auth_router.get("/auth/refresh-access-token")
async def refresh_token():
    pass