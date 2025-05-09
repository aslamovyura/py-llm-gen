from dataclasses import dataclass
from typing import Optional

from src.domain.entities.equipment import Equipment
from src.infrastructure.repositories.equipment import EquipmentRepository
from ...base import Query, QueryHandler

@dataclass
class GetEquipmentQuery(Query):
    equipment_id: int

class GetEquipmentHandler(QueryHandler[GetEquipmentQuery]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, query: GetEquipmentQuery) -> Optional[Equipment]:
        return await self.repository.get_by_id(query.equipment_id) 