from dataclasses import dataclass
from typing import Optional
from ...base import Command, CommandHandler
from src.application.dto.request import RequestUpdateDTO
from src.infrastructure.repositories.request import RequestRepository
from src.domain.entities.request import Request

@dataclass
class UpdateRequestCommand(Command):
    request_id: str
    dto: RequestUpdateDTO

class UpdateRequestHandler(CommandHandler[UpdateRequestCommand]):
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    async def handle(self, command: UpdateRequestCommand) -> Optional[Request]:
        request = await self.repository.get_by_id(command.request_id)
        if not request:
            return None

        update_data = command.dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(request, field, value)

        return await self.repository.update(request) 