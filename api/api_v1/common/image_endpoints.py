from fastapi import APIRouter
from starlette import status
from starlette.responses import FileResponse, JSONResponse

from src.db.db_session import AsyncSessionLocal
from src.exceptions.image_exceptions import ImageNotFoundException
from src.repositories.image_repository import ImageRepository
from src.usecases.get_image_usecase import GetImageUseCase

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get image by id",
)
async def get_image(
        image_id: int,
):
    async with AsyncSessionLocal() as session:
        usecase = GetImageUseCase(
            repository=ImageRepository(session)
        )
    try:
        image = await usecase.get_image(image_id)
        return FileResponse(image.image)
    except ImageNotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': str(e),
                'content': None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': str(e),
                'content': None
            }
        )
