from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....dto.request import CreateRequestDTO
from ....repositories.request import RequestRepository
from ....entities.request import Request

@dataclass
class CreateRequestCommand(Command):
    dto: CreateRequestDTO

class CreateRequestHandler(CommandHandler[CreateRequestCommand]):
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    async def handle(self, command: CreateRequestCommand) -> Request:
        request = Request(
            title=command.dto.title,
            description=command.dto.description,
            client_id=command.dto.client_id,
            equipment_category=command.dto.equipment_category,
            required_specifications=command.dto.required_specifications,
            quantity=command.dto.quantity,
            priority=command.dto.priority,
            status=command.dto.status,
            budget_min=command.dto.budget_min,
            budget_max=command.dto.budget_max,
            currency=command.dto.currency,
            desired_delivery_date=command.dto.desired_delivery_date,
            notes=command.dto.notes,
            tags=command.dto.tags
        )
        return await self.repository.create(request) 