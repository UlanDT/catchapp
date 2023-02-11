import os
from dataclasses import dataclass

from src.exceptions.image_exceptions import ImageNotFoundException
from src.repositories.image_repository import ImageRepository


@dataclass
class GetImageUseCase:
    """Usecase for fetching images."""

    repository: ImageRepository

    async def get_image(self, image_id: int):
        image = await self.repository.get_image_by_id(image_id)
        if not await self.is_file_exists(image.image):
            raise ImageNotFoundException(message="File was not found")
        return image

    async def is_file_exists(self, path):
        return os.path.exists(path)
