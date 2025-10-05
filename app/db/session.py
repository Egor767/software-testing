import logging
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models.order import Base
from app.db.config import DbConfig

logger = logging.getLogger("db-session")

cfg = None
engine = None
AsyncSessionLocal = None


def init_engine():
    global cfg, engine, AsyncSessionLocal
    cfg = DbConfig()
    engine = create_async_engine(cfg.create_url(), echo=True, future=True)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    logger.info(f"Database engine initialized at {cfg.create_url()}")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

