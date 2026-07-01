from pydantic import BaseModel

class PostsIn(BaseModel):
    title: str
    content:str
class CreatePostResponse(BaseModel):
    post_id: str

class PostOut(BaseModel):
    post_id:str
    title: str
    content: str
    created_at: str

