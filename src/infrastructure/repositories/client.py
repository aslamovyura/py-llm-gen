from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.domain.entities.client import Client
from src.infrastructure.database.models import Client as ClientModel
from .base_sql import BaseSQLRepository

class ClientRepository(BaseSQLRepository[ClientModel, Client]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClientModel)

    def _format_phone_number(self, phone: Optional[str]) -> Optional[str]:
        if not phone:
            return None
        # Remove any non-digit characters except '+'
        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        # Ensure it starts with '+' if it doesn't
        if not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        return cleaned

    def _format_tags(self, tags: Optional[Dict]) -> List[str]:
        if not tags:
            return []
        # Convert dictionary to list of strings in format "key: value"
        return [f"{k}: {v}" for k, v in tags.items()]

    def _to_entity(self, db_obj: ClientModel) -> Client:
        return Client(
            id=str(db_obj.id),  # Convert integer ID to string
            name=db_obj.name,
            email=db_obj.email,
            phone_number=self._format_phone_number(db_obj.phone_number),
            address=db_obj.address,
            company_name=db_obj.company_name,
            contact_person=db_obj.contact_person,
            notes=db_obj.notes,
            tags=self._format_tags(db_obj.tags),
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
            is_active=db_obj.is_active
        )

    async def get_by_id(self, client_id: str) -> Optional[Client]:
        try:
            client_id_int = int(client_id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == client_id_int)
        )
        db_obj = result.scalar_one_or_none()
        return self._to_entity(db_obj) if db_obj else None

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
        db_models = result.scalars().all()
        return [self._to_entity(model) for model in db_models]

    async def create(self, entity: Client) -> Optional[Client]:
        try:
            # First check if client with this email already exists
            result = await self.session.execute(
                select(self.model_class).filter(self.model_class.email == entity.email)
            )
            existing = result.scalar_one_or_none()
            if existing:
                return None  # Return None if client with this email already exists

            db_obj = self.model_class(
                name=entity.name,
                email=entity.email,
                phone_number=entity.phone_number,
                address=entity.address,
                company_name=entity.company_name,
                contact_person=entity.contact_person,
                notes=entity.notes,
                tags={tag.split(': ')[0]: tag.split(': ')[1] for tag in entity.tags} if entity.tags else {},
                is_active=entity.is_active
            )
            self.session.add(db_obj)
            await self.session.flush()
            return self._to_entity(db_obj)
        except IntegrityError:
            await self.session.rollback()
            return None

    async def update(self, entity: Client) -> Optional[Client]:
        if not entity.id:
            return None
        try:
            client_id_int = int(entity.id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == client_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        update_data = entity.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'tags':
                value = {tag.split(': ')[0]: tag.split(': ')[1] for tag in value} if value else {}
            setattr(db_obj, field, value)
        
        await self.session.flush()
        return self._to_entity(db_obj)

    async def delete(self, client_id: str) -> bool:
        try:
            client_id_int = int(client_id)  # Convert string ID to integer
        except ValueError:
            return False
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == client_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.flush()
        return True 