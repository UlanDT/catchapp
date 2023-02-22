from dataclasses import dataclass
from typing import Optional

from src.db import ContactDB
from src.exceptions.contact_exceptions import (
    ContactDoesNotExistException,
    ContactNotReadyForBingoException
)
from src.repositories.contact_repository import ContactRepository
from src.repositories.meeting_repository import MeetingRepository
from src.schemas import Contact, Meeting


@dataclass
class GetMeetingSlotsUsecase:
    """Usecase to get 9 meeting slots for user."""

    contact_repository: ContactRepository
    meeting_repository: MeetingRepository

    async def get_meeting_slots(self, user_id: int, contact_id: int) -> Meeting:
        """Get meeting slots for user with given contact_id."""
        contact = await self.contact_repository.get_contact(user_id, contact_id)
        await self.validate_contact(contact)

        return await self.meeting_repository.get_meeting_slots(contact.id)

    async def validate_contact(self, contact: Optional[Contact]):
        if not contact:
            raise ContactDoesNotExistException()
        if contact.status != ContactDB.Status.bingo:
            raise ContactNotReadyForBingoException()
