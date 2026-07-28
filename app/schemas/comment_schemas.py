from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentIn(BaseModel):
    content_id: UUID
    content:str

class CommentOut(BaseModel):
    content_id:UUID
    comment_id:UUID
    author:str = "You"
    content:str
    replies:int = 0
    created_at: datetime

class ResponseComment(BaseModel):
    content_id: UUID
    message: str

class Pagination(BaseModel):
    limit:int = 20
    offset:int = 0

