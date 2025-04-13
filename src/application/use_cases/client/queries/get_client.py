from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from ....repositories.client import ClientRepository
from ....entities.client import Client

@dataclass
class GetClientQuery(Query):
    client_id: str

class GetClientHandler(QueryHandler[GetClientQuery]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, query: GetClientQuery) -> Optional[Client]:
        return await self.repository.get_by_id(query.client_id) 