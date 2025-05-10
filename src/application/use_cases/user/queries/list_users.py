from dataclasses import dataclass
from typing import Optional, List
from ...base import Query, QueryHandler
from src.infrastructure.repositories.user import UserRepository
from src.domain.entities.user import User

@dataclass
class ListUsersQuery(Query):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    skip: int = 0
    limit: int = 100

class ListUsersHandler(QueryHandler[ListUsersQuery]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, query: ListUsersQuery) -> List[User]:
        filters = {}
        if query.username:
            filters['username__icontains'] = query.username
        if query.email:
            filters['email__icontains'] = query.email
        if query.role:
            filters['role'] = query.role

        return await self.repository.list(filters=filters, skip=query.skip, limit=query.limit) 