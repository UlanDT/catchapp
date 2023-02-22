from dataclasses import dataclass

from api.api_v1.response import BingoUserContacts, User
from src.db import ContactDB
from src.repositories.sync_repos import (
    SyncContactRepository,
    SyncUserRepository, SyncMeetingRepository
)
from src.services.datetime_service import DateTimeService


@dataclass
class BingoUsecase:
    contact_repository: SyncContactRepository
    user_repository: SyncUserRepository
    meeting_repository: SyncMeetingRepository
    service: DateTimeService

    def schedule_meeting(self):
        users = self.user_repository.get_all_users()
        for user in users:
            contacts = self.get_contacts_ready_for_bingo(user)

            for contact in contacts:
                slots = self.service.generate_nine_time_slots_for_meeting(
                    user.timezone, contact.user.timezone)
                print(slots)
                self.meeting_repository.update_or_create_slots(contact.id, slots)
                self.contact_repository.update_contact_status(contact.id, ContactDB.Status.bingo)



    def get_contacts_ready_for_bingo(self, user: BingoUserContacts):
        return [contact for contact in user.contacts if
                contact.status in (
                    ContactDB.Status.outdated, None,
                    ContactDB.Status.inactive)]

