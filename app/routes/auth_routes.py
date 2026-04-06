from fastapi import APIRouter
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_service import AuthService
from app.utils.response import success_response

router = APIRouter()


@router.post("/register")
async def register(user: UserRegister):
    result = await AuthService.register(user)
    return success_response(result, "User registered successfully")


@router.post("/login")
async def login(user: UserLogin):
    result = await AuthService.login(user)
    return success_response(result, "Login successful")