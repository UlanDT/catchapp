from dataclasses import dataclass
from datetime import datetime, timedelta

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
        # self.start_bingo()
        self.check_matched_users()
        self.check_for_call()

    def get_contacts_ready_for_bingo(self, user: BingoUserContacts):
        return [contact for contact in user.contacts if
                contact.status in (
                    ContactDB.Status.outdated, None,
                    ContactDB.Status.inactive)]

    def start_bingo(self):
        """Set status to "Bingo Time" for users who are ready for bingo"""
        users = self.user_repository.get_all_users()
        for user in users:
            contacts = self.get_contacts_ready_for_bingo(user)

            for contact in contacts:
                slots = self.service.generate_nine_time_slots_for_meeting(
                    user.timezone, contact.user.timezone)
                print(slots)
                self.meeting_repository.update_or_create_slots(contact.id, slots)
                self.contact_repository.update_contact_status(contact.id, ContactDB.Status.bingo)

    def check_matched_users(self):
        """Check if users have selected meetings and set status to

        1) Scheduled - meeting scheduled both users have chosen similar slots
        2) Failed Bingo - 1 of the contacts didn't participate in bingo or
        datetime of all 9 slots have passed.
        3) Failed Match - both contacts couldn't match at least 1 out of 9 slots
        """
        meetings = self.meeting_repository.get_meeting_slots()

        for meeting in meetings:
            now = datetime.now()

            if meeting.user_data and meeting.contact_data:
                user_selected = meeting.user_data['has_selected']
                contact_selected = meeting.contact_data['has_selected']

                if not user_selected or not contact_selected:
                    last_slot = meeting.slots.get('9')
                    if not last_slot:
                        last_slot = meeting.slots.get('8')
                    if datetime.timestamp(now) > last_slot:
                        self.contact_repository.update_contact_status(meeting.contacts_id, ContactDB.Status.failed_bingo)

                if user_selected and contact_selected:
                    matched_slots = {
                        slot_num: meeting.user_data[slot_num]
                        for slot_num in meeting.user_data
                        if slot_num in meeting.contact_data
                        and meeting.user_data[slot_num] == meeting.contact_data[slot_num]}
                    if matched_slots:
                        ts = datetime.fromtimestamp(matched_slots.get(list(matched_slots.keys())[0]))
                        self.meeting_repository.set_meeting_date(meeting.contacts_id, ts)
                        self.contact_repository.update_contact_status(meeting.contacts_id, ContactDB.Status.scheduled)
                    else:
                        self.contact_repository.update_contact_status(
                            meeting.contacts_id, ContactDB.Status.failed_match)

    def check_for_call(self):
        meetings = self.meeting_repository.get_meeting_slots()
        for meeting in meetings:
            if meeting.contacts.status == ContactDB.Status.scheduled:
                if datetime.now() - timedelta(minutes=5) < meeting.meeting_at < datetime.now() + timedelta(minutes=5):
                    self.contact_repository.update_contact_status(meeting.contacts_id, ContactDB.Status.call)
                elif meeting.meeting_at > datetime.now() + timedelta(minutes=5):
                    self.contact_repository.update_contact_status(meeting.contacts_id, ContactDB.Status.failed_to_call)


