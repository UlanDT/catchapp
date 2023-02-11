from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError
from starlette import status

from core.settings import settings
from src.db import User
from src.db.db_session import AsyncSessionLocal
from src.exceptions.user_exceptions import UserNotFoundException
from src.repositories.user_repository import UserRepository
from src.services.token_service import ALGORITHM

INVALID_AUTHENTICATION_CREDENTIALS = 'Could not validate credentials'
USER_HAS_NO_PERMISSION = 'Недостаточно прав'

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.api_v1_path}/auth/login/'
)


class TokenPayload(BaseModel):
    """Model for token."""
    sub: int


async def get_session():
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_token_data(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.access_token_secret_key,
            algorithms=[ALGORITHM],
        )
        return TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_AUTHENTICATION_CREDENTIALS,
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def get_refresh_token_data(
    token: str = Depends(oauth2_scheme),
) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.refresh_token_secret_key,
            algorithms=[ALGORITHM],
        )
        return TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_AUTHENTICATION_CREDENTIALS,
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def validate_refresh_token_user(
    token: TokenPayload = Depends(get_refresh_token_data),
) -> TokenPayload:
    try:
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            await user_repo.get_user_by_id(token.sub)
        return token
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=INVALID_AUTHENTICATION_CREDENTIALS,
        )


async def validate_token_user(
    token: TokenPayload = Depends(get_token_data),
) -> TokenPayload:
    if not token.sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_AUTHENTICATION_CREDENTIALS,
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return token


async def get_user(
    token: TokenPayload = Depends(validate_token_user),
) -> User:
    try:
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            return await user_repo.get_user_by_id(token.sub)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=INVALID_AUTHENTICATION_CREDENTIALS,
        )
