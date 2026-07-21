from pydantic import BaseModel, Field
from datetime import datetime

class PostIn(BaseModel):
    title: str
    content:str

class PostOut(BaseModel):
    content_id:str
    title: str
    content:str
    likes: int
    comments:int
    replys: int
    created_at: str

class FeedbackOut(BaseModel):
    content_id: str
    message:str