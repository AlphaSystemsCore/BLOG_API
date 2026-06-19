from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
router_auth = APIRouter()

@router_auth.post("/auth/register")
async def register_user():
    pass

@router_auth.get("/auth/verify-email/{email-verification-token}")
async def verify_user_email(email_verification_token: str):
    pass

@router_auth.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass

@router_auth.get("/auth/refresh-access-token")
async def refresh_token():
    pass