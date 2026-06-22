from pydantic import BaseModel, Field, EmailStr

class RegisterUser(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128, min_length=8)