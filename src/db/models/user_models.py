from sqlalchemy import (
    Column, String, func, DateTime, Integer, ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from src.db.db_base_class import Base


class UserDB(Base):
    """Users table."""
    __tablename__ = 'users'

    class StatusChoices:
        """Choices for users' statuses.

        code_sent: code sent from aws sns
        code_correct: user entered correct code from sns
        code_incorrect: user entered incorrect code from sns
        invited: user didn't register, but he got invited by another user
        full_data: user provided full information about himself
        """
        code_sent = 'CODE SENT'
        code_correct = 'CODE CORRECT'
        code_incorrect = 'CODE INCORRECT'
        invited = 'INVITED'
        full_data = 'FULL DATA'

    phone = Column(String(24), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=True, unique=False)
    timezone = Column(Integer, nullable=True)
    hangout_time = Column(Integer, nullable=True)
    image_id = Column(Integer, ForeignKey(
        "images.id", ondelete="CASCADE"), nullable=True)
    status = Column(String(255), nullable=True)
    otp_code = Column(String(4), nullable=True)
    otp_expiration = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    # contacts = relationship('ContactDB', lazy='selectin')

    image = relationship('ImageStorageDB', lazy='selectin')
    contacts = relationship("ContactDB", lazy='selectin', foreign_keys="ContactDB.user_id", backref='contact_user')


class ContactDB(Base):
    """Contacts table."""
    __tablename__ = 'contacts'

    class Status:
        """Status of meeting between two contacts."""
        bingo = 'Bingo Time'  # Bingo started, but haven't been used by neither of contacts status date += 96 if one of the contacts chose 1 of the slots.
        scheduled = 'Scheduled'  #
        call = 'Call'  # from scheduled, happens at the time of meeting.
        failed_bingo = 'Failed Bingo'  #  Failed to match, it happens when datetime of 9 slots have passed
        failed_match = 'Failed Match'
        failed_to_call = 'Failed To Call'  # if both contacts failed to call. from call
        success = 'Success'  # Both contacts are in a meeting. from call
        inactive = 'Inactive'  # from success or failed to ...  hangout_time +- 2 days.
        outdated = 'Outdated'  # Old meetings that are no longer valid

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    contact_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(255), nullable=True)

    user = relationship("UserDB", lazy='selectin', foreign_keys="ContactDB.contact_id")
    meetings = relationship("MeetingDB", uselist=False, back_populates="contacts", lazy='selectin')

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'contact_id',
            name='_user_id_uc'),
    )
