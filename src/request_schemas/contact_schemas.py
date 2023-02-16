from typing import List

from pydantic import BaseModel


class ContactIn(BaseModel):
    """Base Contact schema for request."""
    phone: str
    name: str


class ContactListIn(BaseModel):
    """Schema used for updating user."""
    contacts: List[ContactIn]


class ContactRemoveIdIn(BaseModel):
    """Id of contacts to remove."""
    contact_id: int
