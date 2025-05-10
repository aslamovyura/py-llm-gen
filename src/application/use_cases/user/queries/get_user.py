from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from src.infrastructure.repositories.user import UserRepository
from src.domain.entities.user import User

@dataclass
class GetUserQuery(Query):
    user_id: str

class GetUserHandler(QueryHandler[GetUserQuery]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, query: GetUserQuery) -> Optional[User]:
        return await self.repository.get_by_id(query.user_id) 