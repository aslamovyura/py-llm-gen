from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.request import Request
from src.infrastructure.database.models import Request as RequestModel
from .base_sql import BaseSQLRepository

class RequestRepository(BaseSQLRepository[RequestModel, Request]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RequestModel)

    async def list(self, filters: Dict = None, skip: int = 0, limit: int = 100) -> List[Request]:
        query = select(self.model_class)
        
        if filters:
            for key, value in filters.items():
                if '__gte' in key:
                    field = key.replace('__gte', '')
                    query = query.filter(getattr(self.model_class, field) >= value)
                elif '__lte' in key:
                    field = key.replace('__lte', '')
                    query = query.filter(getattr(self.model_class, field) <= value)
                else:
                    query = query.filter(getattr(self.model_class, key) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()) 