from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth.jwt_handler import get_current_user

user_router = APIRouter(tags=["users"])

@user_router.get("/users/profile")
async def get_profile(user_id:Annotated[str, Depends(get_current_user)]):
    return {
        "msg":"Hello, soon to be implemented"
    }