from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import Config

engine = create_engine(Config.DB_URL)


@asynccontextmanager
async def get_session():
    try:
        async_session = async_sessionmaker(engine, class_=AsyncSession)

        async with async_session() as session:
            yield session
    except:
#        await session.rollback()
        raise
    finally:
#        await session.close()
        pass


def check_db() -> bool:
    sync_engine = create_engine(Config.DB_URL)

    try:
        sync_engine.connect()
        return True
    except SQLAlchemyError:
        return False