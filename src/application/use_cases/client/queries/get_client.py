from dataclasses import dataclass
from typing import Optional

from src.domain.entities.client import Client
from src.infrastructure.repositories.client import ClientRepository
from ...base import Query, QueryHandler

@dataclass
class GetClientQuery(Query):
    client_id: str

class GetClientHandler(QueryHandler[GetClientQuery]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, query: GetClientQuery) -> Optional[Client]:
        return await self.repository.get_by_id(query.client_id) 