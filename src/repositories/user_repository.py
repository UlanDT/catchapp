import logging
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from psycopg2.errorcodes import (
    FOREIGN_KEY_VIOLATION,
)

from api.api_v1.response import User, UserOTP
from src.db import UserDB
from src.exceptions.image_exceptions import ImageNotFoundException
from src.request_schemas.user_schemas import UserIn

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

    async def get_user_otp_by_phone(
            self,
            phone: str
    ) -> UserOTP:
        """Get user by phone."""
        stmt = select(self.model).where(self.model.phone == phone)
        query = await self._db_session.execute(stmt)
        return UserOTP.from_orm(query.scalar())

    async def get_user_by_id(
            self,
            user_id: int
    ) -> User:
        """Get user by id."""
        stmt = select(self.model).where(self.model.id == user_id)
        query = await self._db_session.execute(stmt)
        return User.from_orm(query.scalar())

    async def get_user_db_by_id(
            self,
            user_id: int
    ) -> UserDB:
        """Get user by id."""
        stmt = select(self.model).where(self.model.id == user_id)
        query = await self._db_session.execute(stmt)
        return query.scalar()

    async def update_user(
            self,
            user_in: UserIn,
            user_db: UserDB,
    ) -> User:
        """Update user otp data during sending otp code."""
        try:
            await self._db_session.execute(
                update(self.model).where(self.model.id == user_db.id).values(
                    **user_in.dict(exclude_unset=True)
                )
            )
        except IntegrityError as e:
            await self._db_session.rollback()
            logger.exception(f'Error during updating user: {e.orig.args}')
            if e.orig.sqlstate == FOREIGN_KEY_VIOLATION:
                raise ImageNotFoundException(e.orig.args[0].split('\n')[1])
        await self._db_session.commit()
        await self._db_session.refresh(user_db)
        return User.from_orm(user_db)
