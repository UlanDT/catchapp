from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSON

from src.db.db_base_class import Base


class MeetingDB(Base):
    __tablename__ = 'meetings'

    contacts_id = Column(Integer, ForeignKey(
        "contacts.id", ondelete="CASCADE"), nullable=False)
    meeting_at = Column(DateTime(timezone=True), nullable=True, unique=False)
    user_one = Column(JSON())
    user_two = Column(JSON())