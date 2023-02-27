from dataclasses import dataclass
from typing import Optional

from src.db import ContactDB, MeetingDB
from src.exceptions.contact_exceptions import (
    ContactDoesNotExistException,
    ContactNotReadyForBingoException
)
from src.exceptions.meeting_exceptions import \
    MeetingSlotsAlreadySelectedException
from src.repositories.contact_repository import ContactRepository
from src.repositories.meeting_repository import MeetingRepository
from src.schemas.orm_schemas.contact_schemas import Contact


@dataclass
class SetMeetingSlotsUsecase:
    """Set meeting slots for user."""

    contact_repository: ContactRepository
    meeting_repository: MeetingRepository

    async def set_meeting_slots(
            self,
            user_id: int,
            contact_id: int,
            slots: dict[str, float]
    ):
        contact = await self.contact_repository.get_contact(user_id, contact_id)
        await self.validate_contact(contact)

        meeting_db = await self.meeting_repository.get_meeting_data(contact.id)

        slots.update({"has_selected": True})
        is_user = False
        if user_id == contact.user_id:
            is_user = True
            await self.validate_meeting_status(is_user, meeting_db)
            return await self.meeting_repository.set_meeting_slots_for_user(
                contact.id, slots, meeting_db)

        await self.validate_meeting_status(is_user, meeting_db)
        return await self.meeting_repository.set_meeting_slots_for_contact(
            contact.id, slots, meeting_db)

    async def validate_contact(self, contact: Optional[Contact]):
        if not contact:
            raise ContactDoesNotExistException()
        if contact.status != ContactDB.Status.bingo:
            raise ContactNotReadyForBingoException()

    async def validate_meeting_status(self, is_user: bool, meeting: MeetingDB):
        if is_user:
            if meeting.user_data:
                if meeting.user_data.get("has_selected") is True:
                    raise MeetingSlotsAlreadySelectedException()
        else:
            if meeting.contact_data:
                if meeting.contact_data.get("has_selected") is True:
                    raise MeetingSlotsAlreadySelectedException()
