from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.equipment import Equipment
from src.infrastructure.database.models import Equipment as EquipmentModel
from .base_sql import BaseSQLRepository

class EquipmentRepository(BaseSQLRepository[EquipmentModel, Equipment]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EquipmentModel)

    async def list(self, filters: Dict = None, skip: int = 0, limit: int = 100) -> List[Equipment]:
        query = select(self.model_class)
        
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self.model_class, key) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()) 