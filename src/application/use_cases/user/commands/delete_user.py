from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....repositories.user import UserRepository
from src.infrastructure.di.dependencies import inject_repository

@dataclass
class DeleteUserCommand(Command):
    user_id: str

class DeleteUserHandler(CommandHandler[DeleteUserCommand]):
    @inject_repository('user')
    async def handle(self, command: DeleteUserCommand, user: UserRepository) -> bool:
        return await user.delete(command.user_id) 