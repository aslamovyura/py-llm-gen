from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from src.infrastructure.repositories.request import RequestRepository
from src.domain.entities.request import Request

@dataclass
class GetRequestQuery(Query):
    request_id: str

class GetRequestHandler(QueryHandler[GetRequestQuery]):
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    async def handle(self, query: GetRequestQuery) -> Optional[Request]:
        return await self.repository.get_by_id(query.request_id) 