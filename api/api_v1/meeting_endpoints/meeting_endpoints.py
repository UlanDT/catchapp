from typing import Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from api.api_v1.depends import get_user
from api.api_v1.response import User, MeetingResponse, CommonResponse
from src.db.db_session import AsyncSessionLocal
from src.exceptions.contact_exceptions import ContactDoesNotExistException, \
    ContactNotReadyForBingoException
from src.exceptions.meeting_exceptions import \
    MeetingSlotsAlreadySelectedException, MeetingNotReadyException
from src.repositories.contact_repository import ContactRepository
from src.repositories.meeting_repository import MeetingRepository
from src.usecases.meeting_usecases import (
    GetMeetingSlotsUsecase,
    SetMeetingSlotsUsecase, CallContactUsecase
)


router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get meeting slots for user',
    response_model=MeetingResponse
)
async def get_user_meeting_slots(
        contact_id: int,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = GetMeetingSlotsUsecase(
            contact_repository=ContactRepository(session),
            meeting_repository=MeetingRepository(session)
        )
    try:
        return MeetingResponse(
            success=True,
            message='Success',
            content=await usecase.get_meeting_slots(user.id, contact_id)
        )
    except ContactDoesNotExistException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )
    except ContactNotReadyForBingoException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )


class SlotsIn(BaseModel):
    contact_id: int
    slots: Dict[str, float]


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    description='Set meeting time for user',
    response_model=MeetingResponse
)
async def get_user_contacts(
        slots_in: SlotsIn,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = SetMeetingSlotsUsecase(
            contact_repository=ContactRepository(session),
            meeting_repository=MeetingRepository(session)
        )
    try:
        return MeetingResponse(
            success=True,
            message='Success',
            content=await usecase.set_meeting_slots(
                user.id, slots_in.contact_id, slots_in.slots)
        )
    except ContactDoesNotExistException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )
    except ContactNotReadyForBingoException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )
    except MeetingSlotsAlreadySelectedException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )


@router.post(
    '/call',
    status_code=status.HTTP_200_OK,
    description='Call contact',
    response_model=CommonResponse
)
async def call_cantact(
        contact_id: int,
        user: User = Depends(get_user),
):
    async with AsyncSessionLocal() as session:
        usecase = CallContactUsecase(
            contact_repository=ContactRepository(session),
        )
    try:
        await usecase.call_contact(user.id, contact_id)
    except ContactDoesNotExistException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )
    except MeetingNotReadyException as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'success': False,
                'message': e.message,
                'content': None
            }
        )
    return CommonResponse(
        success=True,
        message='Success',
        content='Changed status from call to success',
    )
