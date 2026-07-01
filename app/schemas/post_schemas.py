from pydantic import BaseModel

class PostsIn(BaseModel):
    title: str
    content:str


