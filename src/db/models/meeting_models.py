from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, TIMESTAMP
from sqlalchemy.orm import relationship

from src.db.db_base_class import Base


class MeetingDB(Base):
    __tablename__ = 'meetings'

    contacts_id = Column(Integer, ForeignKey(
        "contacts.id", ondelete="CASCADE"), nullable=False, unique=True)
    meeting_at = Column(TIMESTAMP(), nullable=True, unique=False)
    user_data = Column(JSON())
    contact_data = Column(JSON())
    slots = Column(JSON())
    contacts = relationship("ContactDB", back_populates="meetings", lazy='selectin')
