from dataclasses import dataclass

from api.api_v1.response import UserContacts, User
from src.repositories.contact_repository import ContactRepository


@dataclass
class GetUserContactsUsecase:
    """Get user contacts usecase."""

    contact_repository: ContactRepository

    async def get_user_contacts(self, user: User) -> UserContacts:
        contacts = await self.contact_repository.get_user_contacts(user.id)
        return UserContacts(
            **user.dict(), contacts=contacts
        )
