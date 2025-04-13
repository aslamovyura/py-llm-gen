from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.factory import RepositoryFactory

class Container:
    def __init__(self):
        self._session: AsyncSession | None = None
        self._repository_factory: RepositoryFactory | None = None

    async def init(self):
        self._session = await anext(get_session())
        self._repository_factory = RepositoryFactory(self._session)

    async def cleanup(self):
        if self._session:
            await self._session.close()

    @property
    def repository_factory(self) -> RepositoryFactory:
        if not self._repository_factory:
            raise RuntimeError("Container not initialized. Call init() first.")
        return self._repository_factory

container = Container() 