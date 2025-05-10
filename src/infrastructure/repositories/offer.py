from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.offer import Offer
from src.infrastructure.database.models import Offer as OfferModel
from .base_sql import BaseSQLRepository

class OfferRepository(BaseSQLRepository[OfferModel, Offer]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OfferModel)

    def _format_additional_services(self, services: Optional[Dict]) -> List[str]:
        if not services:
            return []
        # Convert dictionary to list of enabled services
        return [service for service, enabled in services.items() if enabled]

    def _to_entity(self, db_obj: OfferModel) -> Offer:
        return Offer(
            id=str(db_obj.id),  # Convert integer ID to string
            request_id=db_obj.request_id,
            equipment_id=db_obj.equipment_id,
            price=db_obj.price,
            currency=db_obj.currency,
            quantity=db_obj.quantity,
            delivery_date=db_obj.delivery_date,
            warranty_period_months=db_obj.warranty_period_months,
            status=db_obj.status,
            terms_and_conditions=db_obj.terms_and_conditions,
            notes=db_obj.notes,
            additional_services=self._format_additional_services(db_obj.additional_services),
            discount_percentage=db_obj.discount_percentage,
            payment_terms=db_obj.payment_terms,
            custom_payment_terms=db_obj.custom_payment_terms,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
            is_active=db_obj.is_active
        )

    async def get_by_id(self, offer_id: str) -> Optional[Offer]:
        try:
            offer_id_int = int(offer_id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == offer_id_int)
        )
        db_obj = result.scalar_one_or_none()
        return self._to_entity(db_obj) if db_obj else None

    async def list(self, filters: Dict = None, skip: int = 0, limit: int = 100) -> List[Offer]:
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

    async def create(self, entity: Offer) -> Offer:
        db_obj = self.model_class(
            request_id=entity.request_id,
            equipment_id=entity.equipment_id,
            price=entity.price,
            currency=entity.currency,
            quantity=entity.quantity,
            delivery_date=entity.delivery_date,
            warranty_period_months=entity.warranty_period_months,
            status=entity.status,
            terms_and_conditions=entity.terms_and_conditions,
            notes=entity.notes,
            additional_services={service: True for service in entity.additional_services},
            discount_percentage=entity.discount_percentage,
            payment_terms=entity.payment_terms,
            custom_payment_terms=entity.custom_payment_terms,
            is_active=entity.is_active
        )
        self.session.add(db_obj)
        await self.session.flush()
        return self._to_entity(db_obj)

    async def update(self, entity: Offer) -> Optional[Offer]:
        if not entity.id:
            return None
        try:
            offer_id_int = int(entity.id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == offer_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        update_data = entity.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'additional_services':
                value = {service: True for service in value}
            setattr(db_obj, field, value)
        
        await self.session.flush()
        return self._to_entity(db_obj)

    async def delete(self, offer_id: str) -> bool:
        try:
            offer_id_int = int(offer_id)  # Convert string ID to integer
        except ValueError:
            return False
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == offer_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.flush()
        return True 