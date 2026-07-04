from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.auth.jwt_handler import get_current_user
from app.services.like_service import create_like_service

like_router = APIRouter(tags=["likes"])
# to continue 

@like_router.post("/likes")
def create_like(post_id:str, user_id:Annotated[str, Depends(get_current_user)]):
    message = create_like_service(user_id, post_id)
    return message

