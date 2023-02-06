from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


class Base:

    id = Column(Integer, primary_key=True, index=True, unique=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)


Base = declarative_base(cls=Base)
