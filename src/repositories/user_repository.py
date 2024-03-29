import logging
from datetime import datetime
from typing import List, Dict

from pydantic import parse_obj_as
from sqlalchemy import select, update, delete
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
            otp_expiration=otp_expiration,
            status=UserDB.StatusChoices.code_sent
        )

        self._db_session.add(user_db)
        await self._db_session.commit()
        await self._db_session.refresh(user_db)

    async def delete_user(self, user_id: int) -> None:
        """Delete user."""
        await self._db_session.execute(
            delete(self.model).where(self.model.id == user_id)
        )
        await self._db_session.commit()

    async def update_user_otp(
            self,
            phone: str,
            code: str,
            otp_expiration: datetime
    ) -> None:
        """Update user otp data during sending otp code."""
        await self._db_session.execute(
            update(self.model).where(self.model.phone == phone).values(
                otp_code=code, otp_expiration=otp_expiration,
                status=UserDB.StatusChoices.code_sent
            )
        )
        await self._db_session.commit()

    async def update_user_status(self, phone: str, status: str) -> None:
        await self._db_session.execute(
            update(self.model).where(self.model.phone == phone).values(
                status=status
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
        user_db = query.scalar()
        return UserOTP.from_orm(user_db) if user_db else None

    async def get_user_by_phone(self, phone: str) -> User:
        stmt = select(self.model).where(self.model.phone == phone)
        query = await self._db_session.execute(stmt)
        user_db = query.scalar()
        return User.from_orm(user_db) if user_db else None

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

    async def set_user_fcm_token_and_device(self, user: User, fcm_token: str, device: str):
        """Set user's fcm_token and device."""
        await self._db_session.execute(
            update(self.model).where(self.model.id == user.id).values(
                fcm_token=fcm_token, device=device
            )
        )
        await self._db_session.commit()

    async def get_users_by_phone(self, phones: List[str]) -> List[User]:
        """Get list of users by their phone."""

        stmt = select(self.model).where(self.model.phone.in_(phones))
        query = await self._db_session.execute(stmt)
        return parse_obj_as(List[User], query.scalars().all())

    async def bulk_create_users(self, users_data: List[Dict[str, str]]):
        await self._db_session.run_sync(
            lambda session: session.bulk_insert_mappings(
                self.model, users_data
            ))
        await self._db_session.commit()
