from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from src.infrastructure.repositories.offer import OfferRepository
from src.domain.entities.offer import Offer

@dataclass
class GetOfferQuery(Query):
    offer_id: str

class GetOfferHandler(QueryHandler[GetOfferQuery]):
    def __init__(self, repository: OfferRepository):
        self.repository = repository

    async def handle(self, query: GetOfferQuery) -> Optional[Offer]:
        return await self.repository.get_by_id(query.offer_id) 