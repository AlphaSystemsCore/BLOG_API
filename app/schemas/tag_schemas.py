from pydantic import BaseModel 
from typing import Literal

class TagsIn(BaseModel):
    tag_name: str
    tag_category: Literal['Bitcoin', 'Blockchain', 'Distributed Systems', 'Cryptography', 'Networking', 'Databases']
    