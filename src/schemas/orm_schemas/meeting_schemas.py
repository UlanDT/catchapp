from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel


class Meeting(BaseModel):
    """Schema used to map ContactDB query."""

    id: int
    contacts_id: int
    meeting_at: Optional[datetime]
    user_data: Optional[Dict]
    contact_data: Optional[Dict]
    slots: Optional[Dict]

    class Config:
        orm_mode = True
