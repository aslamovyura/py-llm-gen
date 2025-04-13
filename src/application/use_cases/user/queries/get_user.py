from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from ....repositories.user import UserRepository
from ....entities.user import User
from src.infrastructure.di.dependencies import inject_repository

@dataclass
class GetUserQuery(Query):
    user_id: str

class GetUserHandler(QueryHandler[GetUserQuery]):
    @inject_repository('user')
    async def handle(self, query: GetUserQuery, user: UserRepository) -> Optional[User]:
        return await user.get_by_id(query.user_id) 