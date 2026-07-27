from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated

from app.auth.jwt_handler import get_current_user
from app.schemas.comment_schemas import CommentIn, CommentOut, ResponseComment
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

@comment_router.delete("/comments/{content_id}", response_model=ResponseComment)
def delete_comment(comment_id:str, user_id:Annotated[str, Depends(get_current_user)]):
    try:
        return delete_comment_service(user_id, comment_id)
    except CommentException as e:
        raise HTTPException(
            status_codes = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise UNEXPECTED_ERROR


@comment_router.get("/comments/{content_id}")
def get_all_comments(post_id: str):
    comments = get_all_comments_service(post_id)
    return comments

@comment_router.get("/comments/{post_id}/counts")
def count_comments(post_id):
    count_message = get_total_comment_count_service(post_id)
    return count_message
