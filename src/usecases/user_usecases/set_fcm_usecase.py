from dataclasses import dataclass

from api.api_v1.response import User
from src.exceptions.user_exceptions import IncorrectModelException
from src.repositories.user_repository import UserRepository


@dataclass
class SetFcmUsecase:
    """Usecase to set user's fcm token and device."""

    repository: UserRepository

    async def set_user_fcm(self, user: User, fcm_token: str, device: str):
        """Set user's fcm token and device."""
        if device not in ("android", "ios",):
            raise IncorrectModelException(message="Device should be android or ios")

        await self.repository.set_user_fcm_token_and_device(user, fcm_token, device)
