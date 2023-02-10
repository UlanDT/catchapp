from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class CommonResponse(BaseModel):
    """Common response class."""

    success: bool
    message: str
    content: Optional[dict]
    error: Optional[str]



class LogInOut(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str


class LogInResponse(CommonResponse):
   content: Optional[LogInOut]
