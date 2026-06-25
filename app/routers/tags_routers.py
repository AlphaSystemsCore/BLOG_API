from fastapi import APIRouter, Depends
from typing import Annotated


tag_router = APIRouter(tags=["tags/hashtags"])

@tag_router.get("/tags/")
def get_all_tags(user_id: Annotated[str, Depends(get_current_user)]):
    return {
        "msg":"Hello, to be implemented soon 🙂"
    }