from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.api_v1.response import BingoUserContacts, User
from src.db import UserDB


class SyncUserRepository:
    """Repository for users table."""

    model = UserDB

    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_all_users(self) -> List[BingoUserContacts]:
        stmt = select(self.model).where(self.model.status == self.model.StatusChoices.full_data)
        query = self._db_session.execute(stmt)
        return parse_obj_as(List[BingoUserContacts], query.scalars().all())

    def get_user_by_id(self, user_id: int) -> User:
        stmt = select(self.model).where(self.model.id == user_id)
        query = self._db_session.execute(stmt)
        return User.from_orm(query.scalar())
