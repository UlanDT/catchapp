from typing import Optional

from pydantic import BaseModel


class UserIn(BaseModel):
    """Schema used for updating user."""
    name: Optional[str]
    timezone: Optional[int]
    hangout_time: Optional[int]
    image_id: Optional[int]