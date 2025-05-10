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
        offers = result.scalars().all()
        
        # Transform the data to match entity requirements
        return [
            Offer(
                id=offer.id,
                request_id=offer.request_id,
                equipment_id=offer.equipment_id,
                price=offer.price,
                currency=offer.currency,
                quantity=offer.quantity,
                delivery_date=offer.delivery_date,
                warranty_period_months=offer.warranty_period_months,
                status=offer.status,
                terms_and_conditions=offer.terms_and_conditions,
                notes=offer.notes,
                additional_services=self._format_additional_services(offer.additional_services),
                discount_percentage=offer.discount_percentage,
                payment_terms=offer.payment_terms,
                custom_payment_terms=offer.custom_payment_terms,
                created_at=offer.created_at,
                updated_at=offer.updated_at,
                is_active=offer.is_active
            )
            for offer in offers
        ] 