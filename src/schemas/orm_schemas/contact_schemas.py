from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Contact(BaseModel):
    """Schema used to map ContactDB query."""

    id: int
    user_id: int
    contact_id: int
    status: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

