from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated

from app.auth.jwt_handler import get_current_user
from app.schemas.comment_schemas import CommentIn, CommentOut, ResponseComment, ReplyOut, ReplyIn
from app.services.comment_service import create_comment_service, get_all_comments_service, delete_comment_service, get_total_comment_count_service
from app.exceptions.comment_exception import CommentException


comment_router = APIRouter(tags=["comments"])

UNEXPECTED_ERROR = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED ERROR OCCURED"
        )

@comment_router.post("/comments", response_model=CommentOut)
def create_comment(comment_in:CommentIn, user_id: Annotated[str, Depends(get_current_user)]):
    try:
        return create_comment_service(user_id, comment_in)

    except  CommentException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise UNEXPECTED_ERROR

@comment_router.get("/comments/{content_id}", response_model=CommentOut)
def get_comments(post_id:str):
    """get comments for a post"""
    pass


@comment_router.patch("/comment/{comment_id}")
def update_comment(comment_id:str, user_id: str):
    """update a comment"""


@comment_router.delete("/comments/{comment_id}", response_model=ResponseComment)
def delete_comment(comment_id:str, user_id:Annotated[str, Depends(get_current_user)]):
    """delete comment/reply """
    try:
        return delete_comment_service(user_id, comment_id)
    except CommentException as e:
        raise HTTPException(
            status_codes = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise UNEXPECTED_ERROR


@comment_router.post("/comments/{parent_comment_id}")
def create_reply(reply_in: ReplyIn, user_id: str):
    """reply a comment/reply"""
    pass


@comment_router.get("/comments/{current_parent_comment_id}/replies", response_model=ReplyOut)
def get_replies(current_parent_comment_id):
    """gets replies on the comments or replies"""
    pass



