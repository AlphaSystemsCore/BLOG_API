from pydantic import BaseModel

class PostsIn(BaseModel):
    title: str
    content:str
class CreatePostResponse(BaseModel):
    post_id: str

