from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID
from typing import Literal

from enum import Enum
class By(Enum):
    title = "title"
    comments = "comments"
    replies = "replies"
    likes = "likes"
    author = "author"
    

class PostIn(BaseModel):
    title: str
    content:str

class PostOut(BaseModel):
    content_id:UUID
    title: str
    content:str
    author:str = "You"
    status: str 
    likes: int = 0
    comments:int = 0
    replies: int = 0
    created_at: date

class FeedbackOut(BaseModel):
    content_id: str
    message:str

class Pagination(BaseModel):
    limit: int = Field(default=20, ge=1, le=50)
    offset: int = Field(default=0, ge=0)

class PostFiltersOthers(BaseModel):
    author: str | None = None
    title: str | None = None
    content_id: UUID | None = None
    created_after: date | None = None
    created_before: date| None = None


class SortOptions(BaseModel):
    by: By | str = "created_at"
    direction: Literal["asc", "desc"] = "desc"


class PostSearchOthers(BaseModel):
    filters: PostFiltersOthers = PostFiltersOthers()
    sort: SortOptions = SortOptions()
    pagination: Pagination = Pagination()


class PostFiltersOwner(BaseModel):
    author: str | None = None
    title: str | None = None
    content_id: UUID | None = None
    status: Literal["drafted", "published"] | None = None
    created_after: date | None = None
    created_before: date| None = None

class PostSearchOwner(BaseModel):
    filters: PostFiltersOwner = PostFiltersOwner()
    sort: SortOptions = SortOptions()
    pagination: Pagination = Pagination()

