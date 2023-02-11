from fastapi import APIRouter
from api.api_v1.auth_endpoints import auth_endpoints as auth
from api.api_v1.user_endpoints import user_endpoints as user
from api.api_v1.common import image_endpoints as images

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(images.router, prefix='/image', tags=['image'])
