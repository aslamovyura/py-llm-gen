from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.user import User
from src.infrastructure.database.models import User as UserModel
from .base_sql import BaseSQLRepository

class UserRepository(BaseSQLRepository[UserModel, User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.username == username)
        )
        db_obj = result.scalar_one_or_none()
        return db_obj

    async def list(self, filters: Dict = None, skip: int = 0, limit: int = 100) -> List[User]:
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