from fastapi import Depends, APIRouter, HTTPException, status

from app.schemas.auth_schemas import RegisterUser
auth_router = APIRouter(tags=["Auths"])


@auth_router.post("/auths/register")
async def register_user(user: RegisterUser):
    try:
    except:
        
