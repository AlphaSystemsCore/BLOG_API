from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Literal

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
    created_at: datetime

class FeedbackOut(BaseModel):
    content_id: str
    message:str
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class PostFilters(BaseModel):
    author: str | None = None
    title: str | None = None
    content_id: UUID | None = None
    status: Literal["drafted", "published"] | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None

from enum import Enum
class By(Enum):
    title = "title"
    created_at = "created_at"
    likes = "likes"
    author = "author"
    

class SortOptions(BaseModel):
    by: By | None = None
    direction: Literal["asc", "desc"] = "desc"


class PostSearch(BaseModel):
    filters: PostFilters = PostFilters()
    sort: SortOptions = SortOptions()
    pagination: Pagination = Pagination()
