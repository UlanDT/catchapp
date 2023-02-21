from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.api_v1.response import BingoUserContacts
from src.db import UserDB


class SyncUserRepository:
    """Repository for users table."""

    model = UserDB

    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_all_users(self) -> List[BingoUserContacts]:
        stmt = select(self.model)
        query = self._db_session.execute(stmt)
        return parse_obj_as(List[BingoUserContacts], query.scalars().all())
