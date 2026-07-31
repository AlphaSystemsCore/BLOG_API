from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated, List
from psycopg2 import errors
from uuid import UUID

from app.auth.jwt_handler import get_current_user
from app.schemas.tag_schemas import TagIn, TagOut, TagResponse
from app.services.tag_service import get_tags_service, create_tag_service, delete_tag_service
from app.exceptions.tag_exceptions import TagExceptions


tag_router = APIRouter(tags=["tags/hashtags"])


@tag_router.post("/tags")
def create_tag(tag_in: TagsIn, user_id: Annotated[UUID, Depends(get_current_user)]):
    try:
        return create_tag_service(user_id, tag_in)
    except errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already exists"
        )
    except TagExceptions as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@tag_router.get("/tags", response_model=list[TagOut])
def get_tags():
    try:
        return get_tags_service()
    except TagExceptions as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@tag_router.delete("/tags")
def delete_tag(tag_id:str, user_id: Annotated[str,Depends(get_current_user)]):
    try:
        return delete_tag_service(tag_id)
    except TagNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )