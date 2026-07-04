from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
from app.auth.jwt_handler import get_current_user
from app.schemas.comment_schemas import CommentIn
from app.services.comment_service import create_comment_service, get_all_comments_service, delete_comment_service


comment_router = APIRouter(tags=["comments"])

@comment_router.post("/comments")
def create_comment(comment_in:CommentIn, user_id: Annotated[str, Depends(get_current_user)]):
    comment_id = create_comment_service(user_id, comment_in)
    return comment_id

@comment_router.delete("/comments/{comment_id}")
def delete_comment(comment_id:str, user_id:Annotated[str, Depends(get_current_user)]):
    feedback = delete_comment_service(user_id, comment_id)
    return feedback

@comment_router.get("/comments/{post_id}")
def get_all_comments(post_id: str):
    comments = get_all_comments_service(post_id)
    return comments

    