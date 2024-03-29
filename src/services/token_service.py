from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from jose import jwt

from core.settings import settings

ALGORITHM = 'HS256'


@dataclass
class AuthToken:
    """Class that provides access and refresh tokens."""
    user_id: int
    access_token: str
    refresh_token: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


class AuthTokenService:
    """Service to generate access and refresh tokens."""

    def get_tokens(self, user_id: int):
        """Get access and refresh token."""
        return AuthToken(
            user_id=user_id,
            access_token=self._create_access_token(user_id),
            refresh_token=self._create_refresh_token(user_id)
        ).dict()

    def _create_access_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode = {'exp': expire, 'sub': str(user_id)}
        return jwt.encode(
            to_encode,
            settings.access_token_secret_key,
            algorithm=ALGORITHM)

    def _create_refresh_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.refresh_token_expire_minutes
        )
        to_encode = {'exp': expire, 'sub': str(user_id)}
        return jwt.encode(
            to_encode,
            settings.refresh_token_secret_key,
            algorithm=ALGORITHM)


token_service = AuthTokenService()
