from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

from src.clients.sns_client import sns_client
from src.db.db_session import AsyncSessionLocal
from src.repositories.user_repository import UserRepository
from src.services.datetime_service import datetime_service
from src.services.generate_code import generate_code_service
from src.usecases.auth_usecases import SendCodeUseCase

router = APIRouter()


class PhoneIn(BaseModel):
    """Schema used to send code to provided phone"""
    phone: str


@router.post(
    '/send_code',
    status_code=status.HTTP_200_OK,
    description='Send verification code to provided phone number',

)
async def send_code(phone: PhoneIn):
    """Endpoint to send generated code to users using aws sns."""
    async with AsyncSessionLocal() as session:
        usecase = SendCodeUseCase(
            client=sns_client,
            code_service=generate_code_service,
            datetime_service=datetime_service,
            repository=UserRepository(session)
        )
    return await usecase.send_code(phone.phone)
