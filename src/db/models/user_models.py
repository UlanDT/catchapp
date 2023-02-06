from sqlalchemy import Column, String, func, DateTime, Integer, ForeignKey, \
    UniqueConstraint

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


class ContactDB(Base):
    """Contacts table."""
    __tablename__ = 'contacts'

    user_id1 = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    user_id2 = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            'user_id1', 'user_id2',
            name='_user_id_uc'),
    )
