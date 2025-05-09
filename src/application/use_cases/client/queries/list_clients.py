from dataclasses import dataclass
from typing import Optional, List

from src.domain.entities.client import Client
from src.infrastructure.repositories.client import ClientRepository
from ...base import Query, QueryHandler

@dataclass
class ListClientsQuery(Query):
    name: Optional[str] = None
    email: Optional[str] = None
    company_name: Optional[str] = None
    skip: int = 0
    limit: int = 100

class ListClientsHandler(QueryHandler[ListClientsQuery]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, query: ListClientsQuery) -> List[Client]:
        filters = {}
        if query.name:
            filters['name__icontains'] = query.name
        if query.email:
            filters['email__icontains'] = query.email
        if query.company_name:
            filters['company_name__icontains'] = query.company_name

        return await self.repository.list(filters=filters, skip=query.skip, limit=query.limit) 