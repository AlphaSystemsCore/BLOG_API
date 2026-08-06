from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
from uuid import UUID

from app.exceptions.comment_exception import CommentException
from app.auth.jwt_handler import get_current_user
from app.schemas.comment_schemas import CommentIn, CommentOut, ResponseComment, ReplyOut, ReplyIn, Pagination
from app.services.comment_service import(
    create_comment_service,
    get_comments_service,
    update_comment_service,
    delete_comment_service,
    create_reply_service,
    get_replies_service
    )



comment_router = APIRouter(tags=["comments"])

UNEXPECTED_ERROR = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED ERROR OCCURED"
        )

@comment_router.post("/comments", response_model=CommentOut)
def create_comment(comment_in:CommentIn, user_id: Annotated[UUID, Depends(get_current_user)]):
    try:
        return create_comment_service(user_id, comment_in)
    except CommentException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@comment_router.get("/comments/{post_id}", response_model=CommentOut)
def get_comments(post_id:str, pagination: Annotated[Pagination, Depends()]):
    """get comments for a post"""
    try:
        return get_comments_service(post_id, pagination)
    except CommentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@comment_router.patch("/comment/{comment_id}")
def update_comment(comment_id:str, user_id:Annotated[UUID, Depends(get_current_user)]):
    """update a comment"""
    try:
        return update_comment(comment_id, user_id)
    except CommentException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


@comment_router.delete("/comments/{comment_id}", response_model=ResponseComment)
def delete_comment(comment_id:str, user_id:Annotated[UUID, Depends(get_current_user)]):
    """delete comment/reply """
    try:
        return delete_comment_service(user_id, comment_id)
    except CommentException as e:
        raise HTTPException(
            status_codes = status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@comment_router.post("/comments/{parent_comment_id}")
def create_reply(reply_in: ReplyIn, user_id:Annotated[UUID, Depends(get_current_user)]):
    """reply a comment/reply"""
    try:
        return create_reply_service(user_id, reply_in)
    except CommentException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)

        )


@comment_router.get("/comments/{current_parent_comment_id}/replies", response_model=ReplyOut)
def get_replies(current_parent_comment_id:UUID, pagination:Annotated[Pagination, Depends()]):
    """gets replies on the comments or replies"""
    try: 
        return get_replies_service(current_parent_comment_id)
    except CommentException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )





