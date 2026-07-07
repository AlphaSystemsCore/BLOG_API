from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated, List

from app.auth.jwt_handler import get_current_user
from app.schemas.post_schemas import PostIn, SuccessAction, PostOut, Pagination
from app.services.post_service import create_post_service, get_all_post_service, get_post_by_id_service, get_post_by_title_service, delete_post_service
from app.exceptions.post_exception import *

post_router = APIRouter(tags=["posts"])



@post_router.post("/posts", response_model=SuccessAction)
def create_post(post_in: PostIn, user_id: Annotated[str, Depends(get_current_user)]):
    try:
        return create_post_service(user_id, post_in)
    except FailedToCreatePostError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR_OCCURED"

        )


@post_router.get("/posts/",response_model=List[PostOut])
def get_posts():
    # to implement pagination 
    try:
        return get_all_post_service()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR_OCCURED"
        )

    
@post_router.get("/posts", response_model=PostOut)
def get_post(post_id:Annotated[str, Query()]):
    try:
        return get_post_by_id_service(post_id)
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR_OCCURED"
        )
    

@post_router.get("/posts/by-title", response_model=PostOut)
def get_post_by_title(title:Annotated[str, Query()]):
    try:
        return get_post_by_title_service(title)
    except PostNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR_OCCURED"
        )

    
@post_router.delete("/posts/{post_id}", response_model=SuccessAction)
def delete_post(post_id:str, user_id: Annotated[str, Depends(get_current_user)]):
    try:
        return delete_post_service(user_id, post_id)
    except DeletionFailedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED ERROR OCCURED"
        )


@post_router.patch("/posts/{post_id}/publish", response_model=SuccessAction)
def publish_post(post_id: str, user_id: Annotated[str, Depends(get_current_user)]):
    try:
        return publish_post_service(user_id, post_id)
    except PublishPostFailedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED ERROR OCCURED"
        )

@post_router.patch("/posts/{post_id}")
def update_post(post_id, user_id: Annotated[str, Depends(get_current_user)]):
    # to be implemented
    pass

# @post_router.exception_handler(Exception)
# async def global_exception(request:Request, exc: Exception):
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"message":str(exc)}
#     )