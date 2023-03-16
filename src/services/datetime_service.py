import random
from datetime import datetime, timedelta

import pytz

# should refer to https://www.reddit.com/r/Python/comments/2wd35a/pytz_timezone_fun/ in the future


class DateTimeService:
    """Service that implements datetime operations."""

    SECONDS = [0 * 60, 30 * 60, 60 * 60, 90 * 60, 120 * 60, 150 * 60, 180 * 60]

    async def get_otp_expiration(self) -> datetime:
        return datetime.now(tz=pytz.utc) + timedelta(minutes=3)

    async def otp_active(self, now: datetime, otp_expiration: datetime):
        return now < otp_expiration

    def ceil_dt(self, dt, delta):
        return dt + (datetime.min - dt) % delta

    # передаем целевой час, таймстемп и оффсет таймзоны в часах, получаем ближайшее время когда для этой таймзоны наступит этот час
    def get_closest_hour(self, hour, timestamp, timezone_offset):
        # Get the current time in the specified timezone
        dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.UTC)
        tzOffset = pytz.FixedOffset(timezone_offset * 60)
        dt = dt.astimezone(tzOffset)

        # Calculate the time for the next hour in the specified timezone
        next_hour = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
        if dt.hour >= hour:
            next_hour = next_hour + timedelta(days=1)

        return next_hour.timestamp()

    # передаем два оффсета в часах, таймстемп и границы времени, в ответ получаем None, если время ОК, и один из оффсетов, если для него время выходит за рамки
    def check_time_range(self, timezone_offset1, timezone_offset2, timestamp,
                         start_day_hour, end_day_hour):
        # Convert the Unix timestamp to a datetime object in UTC timezone
        dt_utc = datetime.utcfromtimestamp(timestamp)

        # Convert the datetime object to the two specified timezones
        dt1 = dt_utc + timedelta(hours=timezone_offset1)
        dt2 = dt_utc + timedelta(hours=timezone_offset2)

        # Check whether the time is within the appropriate range in both timezones
        if dt1.hour < start_day_hour or dt1.hour > end_day_hour or (
                dt1.hour == end_day_hour and dt1.minute == 30):
            return timezone_offset1
        elif dt2.hour < start_day_hour or dt2.hour > end_day_hour or (
                dt2.hour == end_day_hour and dt2.minute == 30):
            return timezone_offset2
        else:
            return None

    # ОБЯЗАТЕЛЬНО user_tz < contact_tz
    def generate_slots(self, user_tz: int, contact_tz: int) -> dict[
        int, float]:
        # приведем к ближайшим 30 минутам
        now = self.ceil_dt(datetime.now(), timedelta(minutes=30))
        timestamp = now.timestamp()

        # ограничим 3 сутками
        max_timestamp = timestamp + 72 * 3600
        # сделаем, что первая таймзона меньше второй

        if user_tz > contact_tz:
            user_tz, contact_tz = contact_tz, user_tz

        # определим границы времени
        tz_diff = contact_tz - user_tz
        starting_hour = 10
        ending_hour = 21
        if tz_diff > 8 and tz_diff < 16:
            starting_hour = 9
            ending_hour = 23
            self.SECONDS = [0 * 60, 30 * 60, 60 * 60]
        elif tz_diff > 4:
            starting_hour = 9
            ending_hour = 22
            self.SECONDS = [0 * 60, 30 * 60, 60 * 60, 90 * 60, 120 * 60]

        next_timestamp = timestamp + 2 * 3600
        print(
            f'INITIAL TS: {timestamp}, USER: {(datetime.utcfromtimestamp(timestamp) + timedelta(hours=user_tz)).strftime("%b %d %H:%M:%S %Z")}, CONTACT: {(datetime.utcfromtimestamp(timestamp) + timedelta(hours=contact_tz)).strftime("%b %d %H:%M:%S %Z")}\r\n')

        slots = []
        slot = 0
        for i in range(9):
            # пытаемся поставить следующий слот
            slot = next_timestamp + random.choice(self.SECONDS)
            if slot > max_timestamp:
                break

            # проверяем что в нужном промежутке времени для обоих чуваков
            checkTimeRange = self.check_time_range(user_tz, contact_tz, slot,
                                                   starting_hour, ending_hour)
            if not checkTimeRange is None:
                # print(f'NOT IN RANGE {slot}, USER {(datetime.utcfromtimestamp(slot) + timedelta(hours=user_tz)).strftime("%b %d %H:%M:%S %Z")}, CONTACT {(datetime.utcfromtimestamp(slot) + timedelta(hours=contact_tz)).strftime("%b %d %H:%M:%S %Z")}')

                # если нет, то ищем ближайшee утро
                next_timestamp = self.get_closest_hour(starting_hour, slot,
                                                       checkTimeRange)
                # print(f'{checkTimeRange}, {next_timestamp}, USER {(datetime.utcfromtimestamp(next_timestamp) + timedelta(hours=user_tz)).strftime("%b %d %H:%M:%S %Z")}, CONTACT {(datetime.utcfromtimestamp(next_timestamp) + timedelta(hours=contact_tz)).strftime("%b %d %H:%M:%S %Z")}')
                slot = next_timestamp + random.choice(self.SECONDS)

                # а вдруг и с другой стороны вылезли
                checkTimeRange = self.check_time_range(user_tz, contact_tz,
                                                       slot, starting_hour,
                                                       ending_hour)
                if not checkTimeRange is None:
                    # print(f'NOT IN RANGE {slot}, USER {(datetime.utcfromtimestamp(slot) + timedelta(hours=user_tz)).strftime("%b %d %H:%M:%S %Z")}, CONTACT {(datetime.utcfromtimestamp(slot) + timedelta(hours=contact_tz)).strftime("%b %d %H:%M:%S %Z")}')
                    next_timestamp = self.get_closest_hour(starting_hour, slot,
                                                           checkTimeRange)
                    slot = next_timestamp + random.choice(self.SECONDS)

            slots.append(slot)

            next_timestamp = slot + 2 * 3600
            print(
                f'SLOT #{i} ADDED with TS {slot}, USER {(datetime.utcfromtimestamp(slot) + timedelta(hours=user_tz)).strftime("%b %d %H:%M:%S %Z")}, CONTACT {(datetime.utcfromtimestamp(slot) + timedelta(hours=contact_tz)).strftime("%b %d %H:%M:%S %Z")}\r\n')

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

        print('doing')
        return self.generate_slots(user_timezone, contact_timezone)


datetime_service = DateTimeService()








