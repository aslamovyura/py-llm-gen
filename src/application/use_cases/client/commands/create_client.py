from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....dto.client import CreateClientDTO
from ....repositories.client import ClientRepository
from ....entities.client import Client

@dataclass
class CreateClientCommand(Command):
    dto: CreateClientDTO

class CreateClientHandler(CommandHandler[CreateClientCommand]):
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def handle(self, command: CreateClientCommand) -> Client:
        client = Client(
            name=command.dto.name,
            email=command.dto.email,
            phone_number=command.dto.phone_number,
            address=command.dto.address,
            company_name=command.dto.company_name,
            contact_person=command.dto.contact_person,
            notes=command.dto.notes,
            tags=command.dto.tags
        )
        return await self.repository.create(client) 