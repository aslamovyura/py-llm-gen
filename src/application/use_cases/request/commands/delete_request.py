from dataclasses import dataclass
from ...base import Command, CommandHandler
from src.infrastructure.repositories.request import RequestRepository

@dataclass
class DeleteRequestCommand(Command):
    request_id: str

class DeleteRequestHandler(CommandHandler[DeleteRequestCommand]):
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    async def handle(self, command: DeleteRequestCommand) -> bool:
        return await self.repository.delete(command.request_id) 