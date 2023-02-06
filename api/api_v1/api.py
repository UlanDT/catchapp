from fastapi import APIRouter
from api.api_v1.auth_endpoints import auth_endpoints as auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
