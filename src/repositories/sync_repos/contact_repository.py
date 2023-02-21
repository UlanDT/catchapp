from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from api.api_v1.response import UserContacts
from src.db import ContactDB


class SyncContactRepository:
    """Repository for users table."""

    model = ContactDB

    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_all_contacts(self) -> List[UserContacts]:
        stmt = select(self.model)
        query = self._db_session.execute(stmt)
        return parse_obj_as(List[UserContacts], query.scalars().all())

    def update_contact_status(self, contact_id: int, status: ContactDB.Status):
        stmt = update(self.model).where(self.model.id == contact_id).values(
            status=status
        )
        self._db_session.execute(stmt)
        self._db_session.commit()

