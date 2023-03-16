from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.settings import settings

async_engine = create_async_engine(
    url=settings.postgres_async_url,
    pool_pre_ping=True,
    pool_size=50
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

sync_engine = create_engine(url=settings.postgres_url, pool_size=50)
SessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    class_=Session,
)
