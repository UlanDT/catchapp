from typing import List, Dict

from pydantic import parse_obj_as
from sqlalchemy import select, or_, delete, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import ContactDB
from src.schemas.orm_schemas.contact_schemas import Contact


class ContactRepository:
    """Repository for users table."""

    model = ContactDB

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_user_contacts(self, user_id: int) -> List[Contact]:
        """Get user contacts by user_id."""
        stmt = select(self.model).where(or_(
            self.model.user_id == user_id,
            self.model.contact_id == user_id
        ))
        query = await self._db_session.execute(stmt)
        return parse_obj_as(List[Contact], query.scalars().all())

    async def bulk_create_contacts(self, users_data: List[Dict[str, int]]):
        """Create contacts in bulk."""

        await self._db_session.run_sync(
            lambda session: session.bulk_insert_mappings(
                self.model, users_data
            ))
        await self._db_session.commit()

    async def delete_user_contacts(self, user_id: int, contact_id: int):
        stmt = delete(self.model).where(or_(
            and_(
                self.model.user_id == user_id,
                self.model.contact_id == contact_id
            ), and_(
                self.model.user_id == contact_id,
                self.model.contact_id == user_id
            ))
        )
        await self._db_session.execute(stmt)
        await self._db_session.commit()

    async def get_contact(self, user_id: int, contact_id: int) -> Contact:
        stmt = select(self.model).where(or_(
            and_(
                self.model.user_id == user_id,
                self.model.contact_id == contact_id
            ), and_(
                self.model.user_id == contact_id,
                self.model.contact_id == user_id
            ))
        )
        query = await self._db_session.execute(stmt)
        return Contact.from_orm(query.scalar())

    async def update_contact_status(self, contact_id: int, status: ContactDB.Status):
        stmt = update(self.model).where(self.model.id == contact_id).values(
            status=status
        )
        await self._db_session.execute(stmt)
        await self._db_session.commit()
