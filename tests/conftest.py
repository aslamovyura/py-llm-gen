import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.config import async_session, Base, engine

@pytest.fixture
async def db_session() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with async_session() as session:
            yield session
            await session.rollback()
        await conn.run_sync(Base.metadata.drop_all) 