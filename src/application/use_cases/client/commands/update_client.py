from dataclasses import dataclass
from typing import Optional
from ...base import Command, CommandHandler
from ....dto.client import UpdateClientDTO
from ....repositories.client import ClientRepository
from ....entities.client import Client

@dataclass
class UpdateClientCommand(Command):
    client_id: str
    dto: UpdateClientDTO

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