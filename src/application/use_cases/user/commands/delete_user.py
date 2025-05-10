from dataclasses import dataclass
from ...base import Command, CommandHandler
from src.infrastructure.repositories.user import UserRepository

@dataclass
class DeleteUserCommand(Command):
    user_id: str

class DeleteUserHandler(CommandHandler[DeleteUserCommand]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, command: DeleteUserCommand) -> bool:
        return await self.repository.delete(command.user_id) 