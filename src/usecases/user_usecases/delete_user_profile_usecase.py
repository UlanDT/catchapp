from dataclasses import dataclass

from api.api_v1.response import User
from src.repositories.user_repository import UserRepository


@dataclass
class DeleteUserProfileUsecase:
    """Delete user profile."""

    repository: UserRepository

    async def delete_user_profile(self, user: User) -> None:
        await self.repository.delete_user(user.id)
