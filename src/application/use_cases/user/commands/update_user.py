from dataclasses import dataclass
from typing import Optional
from ...base import Command, CommandHandler
from src.application.dto.user import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository
from src.domain.entities.user import User

@dataclass
class UpdateUserCommand(Command):
    user_id: str
    dto: UserUpdateDTO

class UpdateUserHandler(CommandHandler[UpdateUserCommand]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, command: UpdateUserCommand) -> Optional[User]:
        user_entity = await self.repository.get_by_id(command.user_id)
        if not user_entity:
            return None

        update_data = command.dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_entity, field, value)

        return await self.repository.update(user_entity) 