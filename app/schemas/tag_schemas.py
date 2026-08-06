from pydantic import BaseModel 
from typing import Literal
from uuid import UUID

class TagIn(BaseModel):
    tag_name: str
    tag_category: Literal['Bitcoin', 'Blockchain', 'Distributed Systems', 'Cryptography', 'Networking', 'Databases']
    

class TagOut(BaseModel):
    tag_id: UUID
    tag_name:str
    tag_category:str

class TagResponse(BaseModel):
    tag_id: UUID
    message: str

    