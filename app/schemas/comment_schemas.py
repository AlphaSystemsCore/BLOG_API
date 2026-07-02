from pydantic import BaseModel

class CommentIn(BaseModel):
    content:str
    post_id:str