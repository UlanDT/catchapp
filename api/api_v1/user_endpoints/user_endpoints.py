from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from api.api_v1.depends import get_user
from api.api_v1.response import UserResponse, User
from src.db.db_session import AsyncSessionLocal
from src.exceptions.image_exceptions import ImageNotFoundException
from src.repositories.user_repository import UserRepository
from src.request_schemas.user_schemas import UserIn
from src.usecases.update_user_profile_usecase import UpdateUserProfileUsecase

router = APIRouter()


@router.patch(
    '/',
    status_code=status.HTTP_200_OK,
    description='Update user profile',
    response_model=UserResponse,
)
async def update_user_profile(
        user_in: UserIn,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = UpdateUserProfileUsecase(
            repository=UserRepository(session)
        )
    try:
        return UserResponse(
            success=True,
            message='User profile successfully updated',
            error=None,
            content=await usecase.update_user_profile(
                user_in=user_in,
                user_id=user.id
            ))
    except ImageNotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': str(e),
                'content': None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': str(e),
                'content': None
            }
        )
