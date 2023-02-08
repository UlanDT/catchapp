from datetime import datetime, timedelta

import pytz


class DateTimeService:
    """Service that implements datetime operations."""

    async def get_otp_expiration(self) -> datetime:
        return datetime.now(tz=pytz.utc) + timedelta(minutes=3)

    async def otp_active(self, now: datetime, otp_expiration: datetime):
        return now < otp_expiration


datetime_service = DateTimeService()
