from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from src.infrastructure.repositories.user import UserRepository
from src.domain.entities.user import User

@dataclass
class GetUserByUsernameQuery(Query):
    username: str

class GetUserByUsernameHandler(QueryHandler[GetUserByUsernameQuery]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, query: GetUserByUsernameQuery) -> Optional[User]:
        return await self.repository.get_by_username(query.username) 