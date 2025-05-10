from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
        clients = result.scalars().all()
        
        # Transform the data to match entity requirements
        return [
            Client(
                id=client.id,
                name=client.name,
                email=client.email,
                phone_number=self._format_phone_number(client.phone_number),
                address=client.address,
                company_name=client.company_name,
                contact_person=client.contact_person,
                notes=client.notes,
                tags=self._format_tags(client.tags),
                created_at=client.created_at,
                updated_at=client.updated_at,
                is_active=client.is_active
            )
            for client in clients
        ] 