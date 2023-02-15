from dataclasses import dataclass
from typing import List

from api.api_v1.response import User
from src.exceptions.contact_exceptions import ContactAmountLimitException, \
    ContactAlreadyExistsException
from src.repositories.contact_repository import ContactRepository
from src.repositories.user_repository import UserRepository
from src.request_schemas.contact_schemas import ContactListIn, ContactIn
from src.schemas import Contact


@dataclass
class AddUserContactsUsecase:
    """Usecase for adding user's contacts in bulk."""

    contact_repository: ContactRepository
    user_repository: UserRepository
    contacts_limit: int = 10

    async def add_user_contacts(self, user_id: int,
                                contacts_in: ContactListIn):
        existing_contacts = await self.contact_repository.get_user_contacts(
            user_id=user_id
        )

        existing_users = await self.user_repository.get_users_by_phone(
            [contact.phone for contact in contacts_in.contacts]
        )

        await self._validate_contacts_do_not_exist(
            existing_contacts=existing_contacts,
            existing_users=existing_users
        )

        await self.create_new_users_by_phone(
            existing_users=existing_users,
            contacts=contacts_in.contacts
        )

        users = await self.user_repository.get_users_by_phone(
            [contact.phone for contact in contacts_in.contacts]
        )

        await self.contact_repository.bulk_create_contacts(
            [{"user_id": user_id, "contact_id": user.id} for user in users]
        )

    async def _validate_contacts_do_not_exist(
            self,
            existing_contacts: List[Contact],
            existing_users: List[User]
    ):
        existing_contact_ids = [contact.contact_id for contact in existing_contacts]
        for user in existing_users:
            if user.id in existing_contact_ids:
                raise ContactAlreadyExistsException(
                    message=f'Contact {user.phone} is already present '
                            f'in contact list.'
                )

    async def create_new_users_by_phone(
            self,
            existing_users: List[User],
            contacts: List[ContactIn]
    ):
        """Create new users."""
        new_users = [
            contact for contact in contacts if
            contact.phone not in [user.phone for user in existing_users]
        ]

        await self.user_repository.bulk_create_users(
            [{"phone": user.phone, "name": user.name} for user in new_users]
        )
