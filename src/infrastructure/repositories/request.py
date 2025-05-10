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
        
        return [
            Request(
                id=model.id,
                title=model.title,
                description=model.description,
                client_id=model.client_id,
                equipment_category=self._format_equipment_category(model.equipment_category),
                required_specifications=model.required_specifications,
                quantity=model.quantity,
                priority=self._format_priority(model.priority),
                status=self._format_status(model.status),
                budget_min=model.budget_min,
                budget_max=model.budget_max,
                currency=model.currency,
                desired_delivery_date=model.desired_delivery_date,
                notes=model.notes,
                tags=self._format_tags(model.tags),
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in db_models
        ] 