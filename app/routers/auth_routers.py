from fastapi import Depends, APIRouter, HTTPException, status, Request, Response
from psycopg2 import errors
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.auth_schemas import RegisterUser
from app.exceptions.auth_exception import InvalidEmailVerificationTokenError, EmailNotFoundError, InvalidPasswordError
from app.services.auth_service import register_user_service,  verify_email_service, login_service, create_new_access_and_refresh_token_service
from app.auth.jwt_handler import get_current_user

auth_router = APIRouter(tags=["Auths"])


@auth_router.post("/auths/register")
def register_user(user: RegisterUser):
    try:
        verification_link = register_user_service(user.user_name, user.email, user.password)
    except errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email/username  already exist in the system"
        ) 

    else:
        #returning link for development and testing, later will send link via an email
        return JSONResponse(
            content=verification_link,
            status_code=status.HTTP_201_CREATED
        )

@auth_router.post("/auths/verify-email/{user_id}/{email_verification_token}")
def verify_email(user_id: str, email_verification_token: str):
    print(user_id)
    # try:
    verify_email_service(user_id, email_verification_token)
    # except InvalidEmailVerificationTokenError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Invalid token"
    #     )

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="INTERNAL_SERVER_ERROR"
    #     )
    return {
            "msg":"Email verified successfully"
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
        response = Response(status_code=401)
        response.delete_cookie(key="refresh_token")
        raise HTTPException(
            status_code=400,
            detail="Invalid refresh token, please login"
        )
    
    try:
        new_access_token_jwt, new_refresh_token_jwt = create_new_access_and_refresh_token_service(refresh_token_jwt, client)
        response = JSONResponse(content={
            "access_token":new_access_token_jwt,
            "token_type":"bearer"
        })
    except RefreshTokenAlreadyConsumed as exc:
        response.delete_cookie(key="refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token, please login."
        )
    except HTTPException as exc:
        response.delete_cookie(key="refresh_token")
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token, please login"
        )
    except Exception as exc:
        response.delete_cookie(key="refresh_token")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR_OCCURED"
        )
    else:
        response = JSONResponse(content={
            "access_token":new_access_token_jwt,
            "token_type":"bearer"
        })
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token_jwt,
            httponly=True,
            samesite="strict",
            path="/auths/refresh"
        )
    return response

@auth_router.post("/auths/logout/")
def logout(request: Request):
  
    return {
        "msg":"soon to be implemented"
    }

@auth_router.post("/auths/logout-all-devices")
def logout_all_devices(user_id: Annotated[str, get_current_user]):
    return {
        "msg":"soon to be implemented"
    }
