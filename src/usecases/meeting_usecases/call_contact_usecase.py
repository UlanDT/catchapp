from dataclasses import dataclass

from src.db import ContactDB
from src.exceptions.contact_exceptions import ContactDoesNotExistException
from src.exceptions.meeting_exceptions import MeetingNotReadyException
from src.repositories.contact_repository import ContactRepository


@dataclass
class CallContactUsecase:
    """Call contact usecase."""

    contact_repository: ContactRepository

    async def call_contact(self, user_id: int, contact_id: int):
        contact = await self.contact_repository.get_contact(user_id, contact_id)

        if not contact:
            raise ContactDoesNotExistException(
                f'Contact not found between users {user_id} and {contact_id}'
            )
        if contact.status != ContactDB.Status.call:
            raise MeetingNotReadyException(
                f'Meeting between contacts {user_id} and {contact_id} is not in "call" status'
            )

        await self.contact_repository.update_contact_status(contact.id, ContactDB.Status.success)
