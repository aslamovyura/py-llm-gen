from dataclasses import dataclass
from typing import Optional
from ...base import Query, QueryHandler
from ....repositories.user import UserRepository
from ....entities.user import User
from src.infrastructure.di.dependencies import inject_repository

@dataclass
class GetUserByUsernameQuery(Query):
    username: str

class GetUserByUsernameHandler(QueryHandler[GetUserByUsernameQuery]):
    @inject_repository('user')
    async def handle(self, query: GetUserByUsernameQuery, user: UserRepository) -> Optional[User]:
        return await user.get_by_username(query.username) 