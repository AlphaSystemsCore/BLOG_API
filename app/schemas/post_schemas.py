from pydantic import BaseModel, Field
from datetime import datetime

class PostIn(BaseModel):
    title: str
    content:str

class FieldsToUpdate(BaseModel):
    post_id:str
    title:str | None = None
    content:str | None = None

class CreatePostOut(BaseModel):
    post_id:str
    title:str
    content:str
    created_at:datetime

class PostOut(BaseModel):
    post_id:str
    author:str
    title:str
    content:str
    likes: int
    comments:int 
    created_at: datetime

class SuccessAction(BaseModel):
    post_id:str
    status:str

class Pagination(BaseModel):
    #to implement pagination
    limit: int = Field(50,ge=0, le=50)
    offset: int = Field(0, le=15)
    next_value: int
    previous_value: int
