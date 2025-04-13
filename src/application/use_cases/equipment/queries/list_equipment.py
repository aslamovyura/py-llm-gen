from dataclasses import dataclass
from typing import Optional, List
from ...base import Query, QueryHandler
from ....repositories.equipment import EquipmentRepository
from ....entities.equipment import Equipment

@dataclass
class ListEquipmentQuery(Query):
    category: Optional[str] = None
    status: Optional[str] = None
    manufacturer: Optional[str] = None
    skip: int = 0
    limit: int = 100

class ListEquipmentHandler(QueryHandler[ListEquipmentQuery]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, query: ListEquipmentQuery) -> List[Equipment]:
        filters = {}
        if query.category:
            filters['category'] = query.category
        if query.status:
            filters['status'] = query.status
        if query.manufacturer:
            filters['manufacturer'] = query.manufacturer

        return await self.repository.list(filters=filters, skip=query.skip, limit=query.limit) 