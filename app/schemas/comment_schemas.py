from pydantic import BaseModel
from uuid import UUID

class CommentIn(BaseModel):
    content_id: UUID
    content:str

class CommentOut(BaseModel):
    content_id:UUID
    content:str

class ResponseComment():
    content_id: UUID
    message: str
