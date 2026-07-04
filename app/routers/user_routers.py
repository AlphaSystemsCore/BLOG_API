from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth.jwt_handler import get_current_user

user_router = APIRouter(tags=["users"])

@user_router.get("/users/profile")
async def get_profile(user_id:Annotated[str, Depends(get_current_user)]):
    user_profile_data = get_user_profile_service(user_id)
    return user_profile_data