from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator

from core.settings import settings


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


class Image(BaseModel):
    id: Optional[int]
    image: Optional[str]

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    phone: str
    name: Optional[str]
    timezone: Optional[int]
    hangout_time: Optional[int]
    image: Optional[Image]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

    @root_validator(pre=False)
    def set_media_urls(cls, values):
        image = values.get('image')
        if image:
            image.image = cls.set_absolute_media_url(image.id)
        return values

    @staticmethod
    def set_absolute_media_url(image_id) -> Optional[str]:
        return f'http://{settings.domain_name}{settings.api_v1_path}/image/?image_id={image_id}'


class UserOTP(BaseModel):
    id: int
    phone: str
    name: Optional[str]
    timezone: Optional[int]
    hangout_time: Optional[int]
    image: Optional[Image]
    status: Optional[str]
    otp_code: Optional[str]
    otp_expiration: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserResponse(CommonResponse):
    content: Optional[User]
