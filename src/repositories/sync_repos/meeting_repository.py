from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.db import MeetingDB
from src.schemas.orm_schemas.meeting_schemas import Meeting


class SyncMeetingRepository:
    model = MeetingDB

    def __init__(self, db_session: Session):
        self._db_session = db_session

    def _create_slots(self, contacts_id: int, slots: dict):
        meeting_db = self.model(
            contacts_id=contacts_id,
            slots=slots
        )
        self._db_session.add(meeting_db)
        self._db_session.commit()

    def _update_slots(self, meeting: MeetingDB, slots: dict):
        self._db_session.execute(
            update(self.model).where(self.model.id == meeting.id).values(
                slots=slots
            )
        )
        self._db_session.commit()

    def update_or_create_slots(self, contacts_id: int, slots: dict):
        stmt = select(self.model).where(self.model.contacts_id == contacts_id)
        query = self._db_session.execute(stmt)
        meeting = query.scalar()
        if not meeting:
            self._create_slots(contacts_id, slots)
        else:
            self._update_slots(meeting, slots)

    def get_meeting_slots(self) -> List[Meeting]:
        stmt = select(self.model)
        query = self._db_session.execute(stmt)
        return parse_obj_as(List[Meeting], query.scalars().all())

    def set_meeting_date(self, contacts_id: int, meeting_at):
        stmt = (update(self.model).where(self.model.contacts_id == contacts_id)
                .values(meeting_at=meeting_at))
        self._db_session.execute(stmt)
        self._db_session.commit()
