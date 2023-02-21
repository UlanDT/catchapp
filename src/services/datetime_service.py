import random
from datetime import datetime, timedelta

import pytz

SECONDS = [120 * 60, 150 * 60, 180 * 60, 210 * 60, 240 * 60]


class DateTimeService:
    """Service that implements datetime operations."""

    async def get_otp_expiration(self) -> datetime:
        return datetime.now(tz=pytz.utc) + timedelta(minutes=3)

    async def otp_active(self, now: datetime, otp_expiration: datetime):
        return now < otp_expiration

    def get_current_time(self, tz: int) -> datetime:
        """Get current time in given timezone."""
        return datetime.utcnow() + timedelta(hours=tz)

    def slot_is_valid_for_both_contacts(
            self,
            possible_slot: float,
            user_tz: int,
            contact_tz: int,
            slots: list[float]
    ) -> bool:
        """Slot is valid when possible_slot is between 9AM and 11PM for both users.
        possible_slot argument is utc timestamp."""
        # print(user_tz, contact_tz)
        user_time_in_unix = possible_slot + user_tz * 3600
        contact_time_in_unix = possible_slot + contact_tz * 3600
        # print(user_time_in_unix)
        # print(contact_time_in_unix)

        user_t = datetime.fromtimestamp(user_time_in_unix)
        user_2t = datetime.fromtimestamp(contact_time_in_unix)
        # print(user_t, user_2t)

        slot_valid_for_user = 9 <= user_t.hour <= 23
        slot_valid_for_user_2 = 9 <= user_2t.hour <= 23
        # print(slot_valid_for_user, slot_valid_for_user_2)
        if len(slots) >= 1:
            if (possible_slot - slots[-1]) < 7199:
                return False
        return slot_valid_for_user and slot_valid_for_user_2

    def generate_slot(self, timestamp: float, user_tz, contact_tz, slots: list[float]):
        possible_slot = timestamp

        counter = 0
        while not self.slot_is_valid_for_both_contacts(
                possible_slot, user_tz, contact_tz, slots):
            if counter >= 50:
                break

            possible_slot += random.choice(SECONDS)
        return possible_slot

    def generate_slots(self, user_tz: int, contact_tz: int) -> dict[int, float]:
        now = datetime.utcnow()
        timestamp = (now + timedelta(hours=1)).replace(minute=0).timestamp()

        next_timestamp = timestamp + random.choice(SECONDS)
        print(f'{timestamp}, {next_timestamp}, {next_timestamp-timestamp}')

        slots = []
        for i in range(9):
            slot = self.generate_slot(next_timestamp, user_tz, contact_tz, slots)
            slots.append(slot)
            slots.sort()

        result = dict()
        for slot_num, slot in enumerate(slots):
            result[slot_num + 1] = slot

        return result

    def generate_nine_time_slots_for_meeting(
            self,
            user_timezone: int,
            contact_timezone: int
    ):
        """Generates nine time slots for meeting."""

        user_datetime = self.get_current_time(tz=user_timezone)
        contact_datetime = self.get_current_time(tz=contact_timezone)

        # time_difference = user_datetime - contact_datetime

        return self.generate_slots(user_timezone, contact_timezone)


datetime_service = DateTimeService()
