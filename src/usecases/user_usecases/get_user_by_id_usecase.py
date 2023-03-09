from dataclasses import dataclass

from src.exceptions.user_exceptions import UserNotFoundException
from src.repositories.user_repository import UserRepository


@dataclass
class GetUserByIdUsecase:
    """Usecase to get contact by id."""

    repository: UserRepository

    async def get_user_by_id(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
