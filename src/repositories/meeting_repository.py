from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import MeetingDB
from src.schemas.orm_schemas.meeting_schemas import Meeting


class MeetingRepository:
    """Repository to interact with MeetingDB objects in database."""

    model = MeetingDB

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_meeting_slots(self, contacts_id: int) -> Meeting:
        stmt = select(self.model).where(
            self.model.contacts_id == contacts_id
        )
        query = await self._db_session.execute(stmt)
        return Meeting.from_orm(query.scalar())

    async def get_meeting_data(self, contacts_id: int) -> MeetingDB:
        stmt = select(self.model).where(
            self.model.contacts_id == contacts_id
        )
        query = await self._db_session.execute(stmt)
        return query.scalar()

    async def set_meeting_slots_for_user(
            self,
            contacts_id: int,
            slots: dict,
            meeting_db: MeetingDB
    ):
        await self._db_session.execute(
            update(self.model).where(self.model.contacts_id == contacts_id).values(
                user_data=slots
            )
        )
        await self._db_session.commit()
        await self._db_session.refresh(meeting_db)
        return Meeting.from_orm(meeting_db)

    async def set_meeting_slots_for_contact(
            self,
            contacts_id: int,
            slots: dict,
            meeting_db: MeetingDB
    ):
        await self._db_session.execute(
            update(self.model).where(self.model.contacts_id == contacts_id).values(
                contact_data=slots
            )
        )
        await self._db_session.commit()
        await self._db_session.refresh(meeting_db)
        return Meeting.from_orm(meeting_db)
