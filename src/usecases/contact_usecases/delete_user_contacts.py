from dataclasses import dataclass

from src.repositories.contact_repository import ContactRepository


@dataclass
class DeleteUserContactsUsecase:
    """Usecase for deleting user's contacts."""

    repository: ContactRepository

    async def delete_user_contacts(self, user_id: int, contact_id: int):
        await self.repository.delete_user_contacts(user_id, contact_id)
