from dataclasses import dataclass

from api.api_v1.response import User
from src.db import UserDB
from src.repositories.user_repository import UserRepository
from src.request_schemas.user_schemas import UserIn


@dataclass
class UpdateUserProfileUsecase:
    """UseCase for updating user profile."""

    repository: UserRepository

    async def update_user_profile(
            self,
            user_in: UserIn,
            user: User,
    ):
        user_db = await self.repository.get_user_db_by_id(user.id)
        user = await self.repository.update_user(
            user_in=user_in,
            user_db=user_db,
        )

        if user.status != UserDB.StatusChoices.full_data:
            if user.name and user.hangout_time and user.timezone:
                await self.repository.update_user_status(user.phone, UserDB.StatusChoices.full_data)

        return user
