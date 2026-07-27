from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentIn(BaseModel):
    content_id: UUID
    content:str

class CommentOut(BaseModel):
    content_id:UUID
    comment_id:UUID
    content:str
    created_at: datetime


class ResponseComment():
    content_id: UUID
    message: str
