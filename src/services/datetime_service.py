from datetime import datetime, timedelta


class DateTimeService:
    """Service that implements datetime operations."""

    async def get_otp_expiration(self):
        return datetime.utcnow() + timedelta(minutes=3)


datetime_service = DateTimeService()
