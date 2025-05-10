from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.request import Request
from src.infrastructure.database.models import Request as RequestModel
from .base_sql import BaseSQLRepository

class RequestRepository(BaseSQLRepository[RequestModel, Request]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RequestModel)

    def _format_equipment_category(self, category: str) -> str:
        """Format equipment category to match the required pattern."""
        category_mapping = {
            'safety': 'other',
            'medical': 'other',
            'laboratory': 'other',
            'industrial': 'other',
            'office': 'other'
        }
        return category_mapping.get(category.lower(), 'other')

    def _format_priority(self, priority: str) -> str:
        """Format priority to match the required pattern."""
        priority_mapping = {
            'urgent': 'high',
            'normal': 'medium'
        }
        return priority_mapping.get(priority.lower(), 'medium')

    def _format_status(self, status: str) -> str:
        """Format status to match the required pattern."""
        status_mapping = {
            'in_progress': 'pending'
        }
        return status_mapping.get(status.lower(), 'draft')

    def _format_tags(self, tags: Dict) -> List[str]:
        """Convert tags dictionary to list of strings."""
        if not tags:
            return []
        return [f"{key}: {value}" for key, value in tags.items()]

    def _to_entity(self, db_obj: RequestModel) -> Request:
        return Request(
            id=str(db_obj.id),  # Convert integer ID to string
            title=db_obj.title,
            description=db_obj.description,
            client_id=db_obj.client_id,
            equipment_category=self._format_equipment_category(db_obj.equipment_category),
            required_specifications=db_obj.required_specifications,
            quantity=db_obj.quantity,
            priority=self._format_priority(db_obj.priority),
            status=self._format_status(db_obj.status),
            budget_min=db_obj.budget_min,
            budget_max=db_obj.budget_max,
            currency=db_obj.currency,
            desired_delivery_date=db_obj.desired_delivery_date,
            notes=db_obj.notes,
            tags=self._format_tags(db_obj.tags),
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    async def get_by_id(self, request_id: str) -> Optional[Request]:
        try:
            request_id_int = int(request_id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == request_id_int)
        )
        db_obj = result.scalar_one_or_none()
        return self._to_entity(db_obj) if db_obj else None

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
        db_models = result.scalars().all()
        return [self._to_entity(model) for model in db_models]

    async def create(self, entity: Request) -> Request:
        db_obj = self.model_class(
            title=entity.title,
            description=entity.description,
            client_id=entity.client_id,
            equipment_category=entity.equipment_category,
            required_specifications=entity.required_specifications,
            quantity=entity.quantity,
            priority=entity.priority,
            status=entity.status,
            budget_min=entity.budget_min,
            budget_max=entity.budget_max,
            currency=entity.currency,
            desired_delivery_date=entity.desired_delivery_date,
            notes=entity.notes,
            tags={tag.split(': ')[0]: tag.split(': ')[1] for tag in entity.tags} if entity.tags else {}
        )
        self.session.add(db_obj)
        await self.session.flush()
        return self._to_entity(db_obj)

    async def update(self, entity: Request) -> Optional[Request]:
        if not entity.id:
            return None
        try:
            request_id_int = int(entity.id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == request_id_int)
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

    async def delete(self, request_id: str) -> bool:
        try:
            request_id_int = int(request_id)  # Convert string ID to integer
        except ValueError:
            return False
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == request_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.flush()
        return True 