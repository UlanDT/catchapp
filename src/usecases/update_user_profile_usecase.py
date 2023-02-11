from dataclasses import dataclass

from src.repositories.user_repository import UserRepository
from src.request_schemas.user_schemas import UserIn


@dataclass
class UpdateUserProfileUsecase:
    """UseCase for updating user profile."""

    repository: UserRepository

    async def update_user_profile(
            self,
            user_in: UserIn,
            user_id: int,
    ):
        user_db = await self.repository.get_user_db_by_id(user_id)
        return await self.repository.update_user(
            user_in=user_in,
            user_db=user_db,
        )
