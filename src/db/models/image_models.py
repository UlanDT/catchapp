from sqlalchemy import Column, String

from src.db.db_base_class import Base


class ImageStorageDB(Base):
    __tablename__ = "images"

    image = Column(String(255), nullable=False, unique=True)
