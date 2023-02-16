from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from api.api_v1.depends import get_user
from api.api_v1.response import (
    User, CommonResponse,
    UserContactsResponse
)
from src.db.db_session import AsyncSessionLocal
from src.exceptions.contact_exceptions import ContactAlreadyExistsException
from src.repositories.contact_repository import ContactRepository
from src.repositories.user_repository import UserRepository
from src.request_schemas.contact_schemas import (
    ContactListIn,
    ContactRemoveIdIn
)
from src.usecases.contact_usecases.add_user_contacts import (
    AddUserContactsUsecase
)
from src.usecases.contact_usecases.delete_user_contacts import (
    DeleteUserContactsUsecase
)
from src.usecases.contact_usecases.get_user_contacts import (
    GetUserContactsUsecase
)

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    description='Add user contacts',
    response_model=CommonResponse,
)
async def add_user_contacts(
        contacts_in: ContactListIn,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = AddUserContactsUsecase(
            contact_repository=ContactRepository(session),
            user_repository=UserRepository(session)
        )
    try:
        await usecase.add_user_contacts(
            user_id=user.id,
            contacts_in=contacts_in
        )
    except ContactAlreadyExistsException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )

    return CommonResponse(
        success=True,
        message='Contacts successfully added',
        content=None
    )


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get user contacts',
    response_model=UserContactsResponse,
)
async def get_user_contacts(
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = GetUserContactsUsecase(
            contact_repository=ContactRepository(session),
        )
    return UserContactsResponse(
        success=True,
        message='Success',
        content=await usecase.get_user_contacts(user)
    )


@router.delete(
    '/',
    status_code=status.HTTP_200_OK,
    description="""Delete user contacts.\n
    
    Provide contact_ids or user_ids from list of contacts \n
    depending on current user's id.
    """,
)
async def delete_user_contacts(
        contact_id: ContactRemoveIdIn,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = DeleteUserContactsUsecase(
            repository=ContactRepository(session),
        )

    await usecase.delete_user_contacts(user.id, contact_id.contact_id)
    return CommonResponse(
        success=True,
        message='Contacts successfully deleted',
        content=None
    )
