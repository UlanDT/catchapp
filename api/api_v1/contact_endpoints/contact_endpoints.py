from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from api.api_v1.depends import get_user
from api.api_v1.response import UserResponse, User
from src.db.db_session import AsyncSessionLocal
from src.exceptions.image_exceptions import ImageNotFoundException
from src.exceptions.user_exceptions import UserNotFoundException
from src.repositories.contact_repository import ContactRepository
from src.repositories.user_repository import UserRepository
from src.request_schemas.contact_schemas import ContactListIn
from src.request_schemas.user_schemas import UserIn
from src.usecases.contact_usecases.add_user_contacts import \
    AddUserContactsUsecase
from src.usecases.update_user_profile_usecase import UpdateUserProfileUsecase

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    description='Add user contacts',
    # response_model=UserResponse,
)
async def add_user_contacts(
    contacts_in: ContactListIn,
    user: User = Depends(get_user),
):
    # try:
    async with AsyncSessionLocal() as session:
        usecase = AddUserContactsUsecase(
            contact_repository=ContactRepository(session),
            user_repository=UserRepository(session)
        )
        await usecase.add_user_contacts(
            user_id=user.id,
            contacts_in=contacts_in
        )

    return UserResponse(
        success=True,
        message='User profile successfully updated',
        error=None,
        content=user
    )
    # except UserNotFoundException as e:
    #     return JSONResponse(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         content={
    #             'success': False,
    #             'message': str(e),
    #             'content': None
    #         }
    #     )
    # except Exception as e:
    #     return JSONResponse(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         content={
    #             'success': False,
    #             'message': str(e),
    #             'content': None
    #         }
    #     )
