from dataclasses import dataclass

from src.infrastructure.repositories.client import ClientRepository
from ...base import Command, CommandHandler

@dataclass
class DeleteClientCommand(Command):
    client_id: str

class DeleteClientHandler(CommandHandler[DeleteClientCommand]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, command: DeleteClientCommand) -> bool:
        return await self.repository.delete(command.client_id) 