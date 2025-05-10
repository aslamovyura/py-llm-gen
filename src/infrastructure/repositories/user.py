from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.user import User
from src.infrastructure.database.models import User as UserModel
from .base_sql import BaseSQLRepository

class UserRepository(BaseSQLRepository[UserModel, User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    def _format_phone_number(self, phone: Optional[str]) -> Optional[str]:
        if not phone:
            return None
        # Remove any non-digit characters except '+'
        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        # Ensure it starts with '+'
        if not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        # Remove leading zeros after the plus sign
        if cleaned.startswith('+0'):
            cleaned = '+' + cleaned[2:].lstrip('0')
        return cleaned

    def _to_entity(self, db_obj: UserModel) -> User:
        return User(
            id=str(db_obj.id),  # Convert integer ID to string
            username=db_obj.username,
            email=db_obj.email,
            full_name=db_obj.full_name,
            hashed_password=db_obj.hashed_password,
            role=db_obj.role,
            phone_number=self._format_phone_number(db_obj.phone_number),
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
            is_active=db_obj.is_active
        )

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_id_int = int(user_id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == user_id_int)
        )
        db_obj = result.scalar_one_or_none()
        return self._to_entity(db_obj) if db_obj else None

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.username == username)
        )
        db_obj = result.scalar_one_or_none()
        return self._to_entity(db_obj) if db_obj else None

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
        db_models = result.scalars().all()
        return [self._to_entity(model) for model in db_models]

    async def create(self, entity: User) -> User:
        db_obj = self.model_class(
            username=entity.username,
            email=entity.email,
            full_name=entity.full_name,
            hashed_password=entity.hashed_password,
            role=entity.role,
            phone_number=entity.phone_number,
            is_active=entity.is_active
        )
        self.session.add(db_obj)
        await self.session.flush()
        return self._to_entity(db_obj)

    async def update(self, entity: User) -> Optional[User]:
        if not entity.id:
            return None
        try:
            user_id_int = int(entity.id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == user_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        update_data = entity.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'phone_number':
                value = self._format_phone_number(value)
            setattr(db_obj, field, value)
        
        await self.session.flush()
        return self._to_entity(db_obj)

    async def delete(self, user_id: str) -> bool:
        try:
            user_id_int = int(user_id)  # Convert string ID to integer
        except ValueError:
            return False
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == user_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.flush()
        return True 