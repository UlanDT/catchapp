import logging
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import UserDB, User

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for users table."""

    model = UserDB

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_user_with_otp_code(
            self,
            phone: str,
            code: str,
            otp_expiration: datetime
    ) -> None:
        """Create user during sending otp."""
        user_db = self.model(
            phone=phone,
            otp_code=code,
            otp_expiration=otp_expiration
        )

        self._db_session.add(user_db)
        await self._db_session.commit()
        await self._db_session.refresh(user_db)

    async def update_user_otp(
            self,
            phone: str,
            code: str,
            otp_expiration: datetime
    ) -> None:
        """Update user otp data during sending otp code."""
        await self._db_session.execute(
            update(self.model).where(self.model.phone == phone).values(
                otp_code=code, otp_expiration=otp_expiration
            )
        )
        await self._db_session.commit()

    async def get_user_by_phone(
            self,
            phone: str
    ) -> User:
        """Get user by phone."""
        stmt = select(self.model).where(self.model.phone == phone)
        query = await self._db_session.execute(stmt)
        return User.from_orm(query.scalar())
