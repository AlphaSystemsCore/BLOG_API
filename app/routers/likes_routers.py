from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.auth.jwt_handler import get_current_user
from app.services.like_service import create_like_service, delete_like_service, count_like_service

like_router = APIRouter(tags=["likes"])
# to continue 
# exception to be handled gracefully later

@like_router.post("/likes/{post_id}")
def create_like(post_id:str, user_id:Annotated[str, Depends(get_current_user)]):
    message = create_like_service(user_id, post_id)
    return message

@like_router.delete("/likes/{post_id}")
def delete_like(post_id, user_id: Annotated[str, Depends(get_current_user)]):
    message = delete_like_service(user_id, post_id)
    return message

@like_router.get("/likes/{post_id}/")
def read_likes(post_id):
    count_message = count_like_service(post_id)
    return count_message