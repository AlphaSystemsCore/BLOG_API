from fastapi import APIRouter, Depends, Form, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
auth_router = APIRouter(tags=["Auths"])

from app.auth.jwt_handler import decode_refresh_token, get_current_user
from app.services.auth_service import (
    register_user_service, 
    validate_email_verification_service, 
    login_user_service
    )
from app.schemas.auth_schemas import RegisterUser, AccessRefreshTokenOut
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
    try:
        validate_email_verification_service(user_id, email_verification_token)
    except EmailVerificationTokenExpired as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification token expired"
        )
    except EmailVerificationTokenInvalidError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Verification link already used."
        )
    except EmailVerificationTokenNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT_FOUND !"
        )
    else:
        return {
        "msg":"email verified successfully, proceed to login"
    }

@auth_router.post("/auth/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:

        client = request.headers.get("User-Agent")
        access_token, refresh_token, refresh_token_value = login_user_service(form_data.username, form_data.password, client)
        access_refresh_token = AccessRefreshTokenOut(refresh_token=refresh_token, access_token=access_token )
        response = JSONResponse(content=access_refresh_token.dict())
        response.set_cookie(
            key="refresh_token",
            value=refresh_token_value,
            httponly=True,
            secure=False
        )
    except EmailNotVerifiedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email Must Be Verified"
        )
    except CredentialError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password, please try again"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR"
        )
    else:
        return response

@auth_router.get("/auth/refresh-access-token")
async def refresh_token(request: Request, token_meta:dict = Depends(decode_refresh_token) ):
    # to continue from here 
    print(token_meta)
    print(request.cookies.get("refresh_token"))
    
@auth_router.get("/auth/logout")
async def logout_user(user_id:str = Depends(get_current_user)):
    # delete continue 
    # revoke the session
    return{
        "msg": "logging user out ..."
    }