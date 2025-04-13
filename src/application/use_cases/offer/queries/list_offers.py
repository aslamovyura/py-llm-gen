from dataclasses import dataclass
from typing import Optional, List
from ...base import Query, QueryHandler
from ....repositories.offer import OfferRepository
from ....entities.offer import Offer

@dataclass
class ListOffersQuery(Query):
    request_id: Optional[int] = None
    equipment_id: Optional[int] = None
    status: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    skip: int = 0
    limit: int = 100

class ListOffersHandler(QueryHandler[ListOffersQuery]):
    def __init__(self, repository: OfferRepository):
        self.repository = repository

    async def handle(self, query: ListOffersQuery) -> List[Offer]:
        filters = {}
        if query.request_id:
            filters['request_id'] = query.request_id
        if query.equipment_id:
            filters['equipment_id'] = query.equipment_id
        if query.status:
            filters['status'] = query.status
        if query.min_price is not None:
            filters['price__gte'] = query.min_price
        if query.max_price is not None:
            filters['price__lte'] = query.max_price

        return await self.repository.list(filters=filters, skip=query.skip, limit=query.limit) 