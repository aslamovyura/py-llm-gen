from dataclasses import dataclass
from typing import Optional
from ...base import Command, CommandHandler
from src.application.dto.user import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository
from src.domain.entities.user import User
from src.infrastructure.di.dependencies import inject_repository

@dataclass
class UpdateUserCommand(Command):
    user_id: str
    dto: UserUpdateDTO

class UpdateUserHandler(CommandHandler[UpdateUserCommand]):
    @inject_repository('user')
    async def handle(self, command: UpdateUserCommand, user: UserRepository) -> Optional[User]:
        user_entity = await user.get_by_id(command.user_id)
        if not user_entity:
            return None

        update_data = command.dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_entity, field, value)

        return await user.update(user_entity) 