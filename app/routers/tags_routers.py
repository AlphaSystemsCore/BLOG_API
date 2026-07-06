from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from psycopg2 import errors

from app.auth.jwt_handler import get_current_user
from app.schemas.tag_schemas import TagsIn
from app.services.tag_service import get_tags_service, create_tag_service, delete_tag_service
from app.exceptions.tag_exceptions import TagNotFoundError


tag_router = APIRouter(tags=["tags/hashtags"])

@tag_router.get("/tags")
def get_tags(user_id: Annotated[str, Depends(get_current_user)]):
    try:
        tags = get_tags_service()
    except TagNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    else:
        return {"tags": tags}
  
@tag_router.post("/tags")
def create_tag(tag: TagsIn, user_id: Annotated[str, Depends(get_current_user)]):
    try:
        create_tag_service(user_id, tag.tag_name, tag.tag_category)
    except errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag already exists"
        )
    else: 
        return {
            "msg": f"{tag.tag_name}, created successfully."
        }

@tag_router.delete("/tags")
def delete_tag(tag_id:str, user_id: Annotated[str, get_current_user]):
    try:
        delete_tag_service(tag_id)
    except TagNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )