from fastapi import Depends, APIRouter, HTTPException, status, Request, Response
from psycopg2 import errors
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import EmailStr

from app.schemas.auth_schemas import RegisterUser
from app.exceptions.auth_exception import *
from app.services.auth_service import (
    register_user_service,   
    verify_email_service, 
    login_service, 
    create_new_access_and_refresh_token_service,
    resend_email_verification_token,
)
from app.auth.jwt_handler import get_current_user

auth_router = APIRouter(tags=["Auths"])


@auth_router.post("/auths/register")
def register_user(user: RegisterUser):
    try:
        verification_link = register_user_service(user.user_name, user.email, user.password)
    except RegistrationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except errors.UniqueViolation as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="EMAIL OR USERNAME ALREADY EXISTS"
        ) 

    else:
        #returning link for development and testing, later will send link via an email
        return JSONResponse(
            content=verification_link,
            status_code=status.HTTP_201_CREATED
        )

@auth_router.get("/auths/verify-email/{user_id}/{email_verification_token}")
def verify_email(user_id: str, email_verification_token: str):
    try:
        feedback = verify_email_service(user_id, email_verification_token)
    except InvalidEmailVerificationTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except InvalidUserIdError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL_SERVER_ERROR"
        )
    return {
        "msg":feedback
    }

@auth_router.post("/auths/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    AuthCredentialError = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password or email, please try again"
        )
    
    client = request.headers.get('User-Agent')
    try:
        refresh_token, access_token = login_service(form_data.username, form_data.password, client)
        response = JSONResponse(content={"access_token": access_token, "token_type":"bearer"})
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="strict",
            path="/auths/refresh"
        )
    except EmailNotFoundError:
        raise AuthCredentialError
    except InvalidPasswordError:
        raise CredentialError
    except Exception as exc:
        # TO LOG ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR"
        )
    else:
        return response

@auth_router.post("/auths/refresh")
def refresh(request: Request):
    client = request.headers.get("User-Agent")
    refresh_token_jwt = request.cookies.get("refresh_token")
    if refresh_token_jwt is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="REFRESH TOKEN NOT FOUND, PLEASE LOGIN"
        )
    try:
        new_access_token_jwt, new_refresh_token_jwt = create_new_access_and_refresh_token_service(refresh_token_jwt, client)
    except RefreshTokenAlreadyConsumed as e:       
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    response = JSONResponse(
        content={
            "access_token":new_access_token_jwt,
            "token_type":"bearer"
            },
            status_code=status.HTTP_201_CREATED    
            )
    response.set_cookie(
        key="refresh_token",
        value=new_access_token_jwt,
        httponly=True,
        samesite='lax',
        secure=True,
        path="/auths/refresh"
    )
    return response

@auth_router.get("/auths/resend-token/{email}")
def resend_token(email:EmailStr):
    try:
        return resend_email_verification_token(email)
    except FailedToCreateVerificationLinkError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Link still active or wrong email"
        )
    except EmailLookUpError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@auth_router.post("/auths/logout/")
def logout(request: Request):
    return "to be implemented"
    

@auth_router.post("/auths/logout-all-devices")
def logout_all_devices(user_id: Annotated[str, get_current_user]):
    return {
        "msg":"soon to be implemented"
    }
