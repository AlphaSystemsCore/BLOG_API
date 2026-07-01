from pydantic import BaseModel

class PostsIn(BaseModel):
    title: str
    content:str
    

class PostOut(BaseModel):
    post_id: str
    user_name: str
    title: str
    content: str
    image_link:str | None = None
    video_link:str | None = None
