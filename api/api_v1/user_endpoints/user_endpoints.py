from fastapi import APIRouter, Depends
from pydantic.main import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from api.api_v1.depends import get_user
from api.api_v1.response import UserResponse, User, UserContactsResponse, CommonResponse
from src.clients.firebase import FirebaseClient
from src.db.db_session import AsyncSessionLocal
from src.exceptions.image_exceptions import ImageNotFoundException
from src.exceptions.user_exceptions import UserNotFoundException, IncorrectModelException
from src.repositories.user_repository import UserRepository
from src.request_schemas.user_schemas import UserIn
from src.usecases.update_user_profile_usecase import UpdateUserProfileUsecase
from src.usecases.user_usecases.delete_user_profile_usecase import DeleteUserProfileUsecase
from src.usecases.user_usecases.get_user_by_id_usecase import GetUserByIdUsecase
from src.usecases.user_usecases.set_fcm_usecase import SetFcmUsecase

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get user profile',
    response_model=UserResponse,
)
async def get_user_profile(
        user: User = Depends(get_user),
):
    try:
        return UserResponse(
            success=True,
            message='Success',
            error=None,
            content=user
        )
    except UserNotFoundException as e:
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


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    description='Get user by id',
    response_model=UserContactsResponse,
    dependencies=[Depends(get_user)]
)
async def get_user_by_id(
        user_id: int,
):
    async with AsyncSessionLocal() as session:
        usecase = GetUserByIdUsecase(
            repository=UserRepository(session),
        )
    try:
        user = await usecase.get_user_by_id(user_id)
    except UserNotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )
    return UserContactsResponse(
        success=True,
        message='Success',
        content=user
    )


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
                user=user
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
    except UserNotFoundException as e:
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


@router.delete(
    '/',
    status_code=status.HTTP_200_OK,
    description='Delete user profile',
)
async def delete_user_profile(
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = DeleteUserProfileUsecase(
            repository=UserRepository(session)
        )
        await usecase.delete_user_profile(user)
        return CommonResponse(
            success=True,
            message="User has been deleted.",
        )


class UserFcmIn(BaseModel):
    """Schema for fcm token and phone model."""

    fcm_token: str
    device: str


@router.patch(
    '/fcm',
    status_code=status.HTTP_200_OK,
    description='Set user fcm token and phone model',
)
async def set_user_fcm(
        phone_data: UserFcmIn,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = SetFcmUsecase(
            repository=UserRepository(session)
        )
    try:
        return UserResponse(
            success=True,
            message='Fcm token successfully updated',
            error=None,
            content=await usecase.set_user_fcm(
                user=user,
                fcm_token=phone_data.fcm_token,
                device=phone_data.device
            ))
    except IncorrectModelException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
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

@router.post(
    '/test/',
    status_code=status.HTTP_200_OK,
)
async def send_token():
    a = FirebaseClient(fcm_token='dPeZpbm9RSqzM9ULa9l9oS:APA91bFyCaj98veBjrxqjzwU5YUmCbd_KcjKPctwp64Tykl4ValPWykc5xO24Nw4c_nays8jWBihZi0JOEEBEANbZq_pnr0HAJNYPG2qkd1NzEl_OQUanMrTN3CSgduCyYTXwGfKO9bF',
                   title='Testing catchapp push', body='Testing catchapp push notifications')
    a.send_android_push_notification()
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'success': True,
                'content': None
            }
        )