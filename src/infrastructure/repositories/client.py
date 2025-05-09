from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.client import Client
from src.infrastructure.database.models import Client as ClientModel
from .base_sql import BaseSQLRepository

class ClientRepository(BaseSQLRepository[ClientModel, Client]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClientModel)

    async def list(self, filters: Dict = None, skip: int = 0, limit: int = 100) -> List[Client]:
        query = select(self.model_class)
        
        if filters:
            for key, value in filters.items():
                if '__icontains' in key:
                    field = key.replace('__icontains', '')
                    query = query.filter(getattr(self.model_class, field).ilike(f'%{value}%'))
                else:
                    query = query.filter(getattr(self.model_class, key) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()) 