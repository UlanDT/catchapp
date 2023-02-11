from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommonResponse(BaseModel):
    """Common response class."""

    success: bool
    message: str
    content: Optional[dict]


class LogInOut(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class LogInResponse(CommonResponse):
   content: Optional[LogInOut]


class User(BaseModel):
    id: int
    phone: str
    name: Optional[str]
    timezone: Optional[int]
    hangout_time: Optional[int]
    image_id: Optional[int]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserResponse(CommonResponse):
    content: Optional[User]
