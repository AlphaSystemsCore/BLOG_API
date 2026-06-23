from pydantic import BaseModel, Field, EmailStr

class RegisterUser(BaseModel):
    user_name: str
    email: EmailStr
    password: str = Field(max_length=128, min_length=8)

class AccessRefreshTokenOut(BaseModel):
    access_token: str | None = None
    refresh_token: str 
    token_type:str =  "bearer"