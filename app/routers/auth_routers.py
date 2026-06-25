from fastapi import Depends, APIRouter, HTTPException, status
from psycopg2 import errors
from fastapi.responses import JSONResponse

from app.schemas.auth_schemas import RegisterUser
from app.services.auth_service import register_user_service, email_formater_service
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
    # except Exception as exc:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail= "INTERNAL_SERVER_ERROR"
    #     )
    else:
        #returning link for development and testing, later will send link to email
        return JSONResponse(
            content=verification_link,
            status_code=status.HTTP_201_CREATED
        )

@auth_router.get("/auths/verify-email/{user_id}/{email_verification_token}")
def verify_email(user_id: str, email_verification_token: str):
    return {
        "msg":"email verified proceed to login, at your comfort"
        ,"token":email_verification_token
    }