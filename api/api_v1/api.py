from fastapi import APIRouter
from api.api_v1.auth_endpoints import auth_endpoints as auth
from api.api_v1.user_endpoints import user_endpoints as user
from api.api_v1.contact_endpoints import contact_endpoints as contacts
from api.api_v1.meeting_endpoints import meeting_endpoints as meetings
from api.api_v1.common import image_endpoints as images
from api.api_v1.common import privacy_endpoints as privacy

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(contacts.router, prefix='/contacts', tags=['contacts'])
api_router.include_router(meetings.router, prefix='/meetings', tags=['meetings'])
api_router.include_router(images.router, prefix='/image', tags=['image'])
api_router.include_router(privacy.router, prefix='/privacy', tags=['privacy'])
