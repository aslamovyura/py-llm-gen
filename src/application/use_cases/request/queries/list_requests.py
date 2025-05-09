from dataclasses import dataclass
from typing import Optional, List
from ...base import Query, QueryHandler
from src.infrastructure.repositories.request import RequestRepository
from src.domain.entities.request import Request

@dataclass
class ListRequestsQuery(Query):
    client_id: Optional[int] = None
    equipment_category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    skip: int = 0
    limit: int = 100

class ListRequestsHandler(QueryHandler[ListRequestsQuery]):
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    async def handle(self, query: ListRequestsQuery) -> List[Request]:
        filters = {}
        if query.client_id:
            filters['client_id'] = query.client_id
        if query.equipment_category:
            filters['equipment_category'] = query.equipment_category
        if query.status:
            filters['status'] = query.status
        if query.priority:
            filters['priority'] = query.priority
        if query.min_budget is not None:
            filters['budget_min__gte'] = query.min_budget
        if query.max_budget is not None:
            filters['budget_max__lte'] = query.max_budget

        return await self.repository.list(filters=filters, skip=query.skip, limit=query.limit) 