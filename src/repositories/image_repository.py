from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.response import Image
from src.db import ImageStorageDB


class ImageRepository:
    """Repository for images table."""

    model = ImageStorageDB

    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def get_image_by_id(self, image_id: int) -> Image:
        stmt = select(self.model).where(self.model.id == image_id)
        query = await self._db_session.execute(stmt)
        return Image.from_orm(query.scalar())
