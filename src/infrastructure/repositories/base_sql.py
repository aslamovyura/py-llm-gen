from typing import Generic, TypeVar, Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.domain.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
EntityType = TypeVar("EntityType")

class BaseSQLRepository(BaseRepository[EntityType], Generic[ModelType, EntityType]):
    def __init__(self, session: AsyncSession, model_class: Type[ModelType]):
        self.session = session
        self.model_class = model_class

    async def get(self, id: int) -> Optional[EntityType]:
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == id)
        )
        db_obj = result.scalar_one_or_none()
        return db_obj

    async def get_all(self) -> List[EntityType]:
        result = await self.session.execute(select(self.model_class))
        return list(result.scalars().all())

    async def add(self, entity: EntityType) -> EntityType:
        db_obj = self.model_class(**entity.model_dump())
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def update(self, entity: EntityType) -> Optional[EntityType]:
        if not entity.id:
            return None
        db_obj = await self.get(entity.id)
        if not db_obj:
            return None
        
        obj_data = entity.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        await self.session.flush()
        return db_obj

    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            delete(self.model_class).where(self.model_class.id == id)
        )
        return result.rowcount > 0 