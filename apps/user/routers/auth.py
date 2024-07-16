from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from apps.user.schemas.user import UserSchema
user_router = APIRouter()


@user_router.post('/login', tags=['Auth'])
def login(user: UserSchema):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
    return JSONResponse(content=token, status_code=200)
