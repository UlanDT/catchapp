from typing import List, Dict

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import ContactDB
from src.schemas import Contact


class ContactRepository:
    """Repository for users table."""

    model = ContactDB

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_user_contacts_by_user_id(
            self,
            user_id: int
    ) -> List[Contact]:
        """Get user contacts by user_id."""
        stmt = select(self.model).where(self.model.user_id == user_id)
        query = await self._db_session.execute(stmt)
        return parse_obj_as(List[Contact], query.scalars().all())

    async def bulk_create_contacts(self, users_data: List[Dict[str, str]]):
        """Create contacts in bulk."""

        await self._db_session.run_sync(
            lambda session: session.bulk_insert_mappings(
                self.model, users_data
            ))
        await self._db_session.commit()

