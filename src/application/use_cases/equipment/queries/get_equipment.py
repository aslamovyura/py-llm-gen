from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from ....repositories.equipment import EquipmentRepository
from ....entities.equipment import Equipment

@dataclass
class GetEquipmentQuery(Query):
    equipment_id: str

class GetEquipmentHandler(QueryHandler[GetEquipmentQuery]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, query: GetEquipmentQuery) -> Optional[Equipment]:
        return await self.repository.get_by_id(query.equipment_id) 