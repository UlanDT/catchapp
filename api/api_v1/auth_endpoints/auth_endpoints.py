from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

from src.clients.sns_client import sns_client
from src.db.db_session import AsyncSessionLocal
from src.repositories.user_repository import UserRepository
from src.services.datetime_service import datetime_service
from src.services.generate_code import generate_code_service
from src.services.token_service import token_service
from src.usecases import SendCodeUseCase, LogInUsecase

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
    # TODO need to return response, to be discussed with client side
    async with AsyncSessionLocal() as session:
        usecase = SendCodeUseCase(
            client=sns_client,
            code_service=generate_code_service,
            datetime_service=datetime_service,
            repository=UserRepository(session)
        )
    return await usecase.process_send_code(phone.phone)


class LogIn(BaseModel):
    """Schema used for loging in."""
    phone: str
    code: str


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    description='Get access and refresh tokens',
)
async def login(login_schema: LogIn):
    """Endpoint to get access/refresh token in exchange for correct code."""
    async with AsyncSessionLocal() as session:
        usecase = LogInUsecase(
            repository=UserRepository(session),
            datetime_service=datetime_service,
            token_service=token_service
        )
    return await usecase.process_login(login_schema.phone, login_schema.code)
