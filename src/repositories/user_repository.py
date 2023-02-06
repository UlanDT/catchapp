import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db import UserDB

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for users table."""

    model = UserDB

    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create_user_with_otp_code(
            self,
            phone: str,
            code: str,
            otp_expiration: datetime
    ):
        user_db = self.model(
            phone=phone,
            otp_code=code,
            otp_expiration=otp_expiration
        )

        self._db_session.add(user_db)
        await self._db_session.commit()
        await self._db_session.refresh(user_db)

    async def get_user_by_phone(
            self,
            phone: str
    ):
        stmt = select(self.model).where(self.model.phone == phone)
        query = await self._db_session.execute(stmt)
        return query.scalar()
