from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....repositories.client import ClientRepository

@dataclass
class DeleteClientCommand(Command):
    client_id: str

class DeleteClientHandler(CommandHandler[DeleteClientCommand]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, command: DeleteClientCommand) -> bool:
        return await self.repository.delete(command.client_id) 