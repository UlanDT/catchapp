from fastapi import APIRouter
from api.api_v1.test_endpoints import test as test

api_router = APIRouter()

api_router.include_router(test.router, prefix='/test', tags=['auth'])

