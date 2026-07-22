from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

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
    replys: int = 0
    created_at: datetime

class FeedbackOut(BaseModel):
    content_id: str
    message:str

class Query(BaseModel):
    author: str | None = None
    title: str | None = None
    content_id: str | None = None
    limit: int = Field(20, le=25)
    offset: int = Field(0, le=20)


