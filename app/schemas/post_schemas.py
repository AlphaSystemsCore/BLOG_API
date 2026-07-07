from pydantic import BaseModel
from datetime import datetime

class PostsIn(BaseModel):
    title: str
    content:str

class PostOut(BaseModel):
    post_id:str
    title:str
    content:str
    created_at: datetime

class SuccessAction(BaseModel):
    post_id:str
    status:str
