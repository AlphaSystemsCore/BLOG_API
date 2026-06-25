from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth.jwt_handler import get_current_user
from app.schemas.tag_schemas import TagsIn

tag_router = APIRouter(tags=["tags/hashtags"])

@tag_router.get("/tags/")
def get_all_tags(user_id: Annotated[str, Depends(get_current_user)]):
    return {
        "msg":"Hello, to be implemented soon 🙂"
    }
@tag_router.post("/tags/")
def create_tag(tag: Tags):
