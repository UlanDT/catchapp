from fastapi import APIRouter
from starlette import status
from starlette.responses import FileResponse, JSONResponse, HTMLResponse

from core.settings import settings


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="privacy html",
)
async def get_privacy():
    return FileResponse(status_code=200, path=f"{settings.base_dir}/privacy.html")
