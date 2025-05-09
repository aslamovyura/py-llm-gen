from dataclasses import dataclass
from typing import Optional
from src.application.dto.client import ClientUpdateDTO
from src.domain.entities.client import Client
from src.infrastructure.repositories.client import ClientRepository
from ...base import Command, CommandHandler

@dataclass
class UpdateClientCommand(Command):
    client_id: str
    dto: ClientUpdateDTO

class UpdateClientHandler(CommandHandler[UpdateClientCommand]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, command: UpdateClientCommand) -> Optional[Client]:
        client = await self.repository.get_by_id(command.client_id)
        if not client:
            return None

        update_data = command.dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)

        return await self.repository.update(client) 