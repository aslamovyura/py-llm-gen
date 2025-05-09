from dataclasses import dataclass

from src.domain.entities.equipment import Equipment
from src.infrastructure.repositories.equipment import EquipmentRepository
from ...base import Command, CommandHandler
from src.application.dto.equipment import EquipmentCreateDTO

@dataclass
class CreateEquipmentCommand(Command):
    dto: EquipmentCreateDTO

class CreateEquipmentHandler(CommandHandler[CreateEquipmentCommand]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, command: CreateEquipmentCommand) -> Equipment:
        equipment = Equipment(
            name=command.dto.name,
            model=command.dto.model,
            serial_number=command.dto.serial_number,
            manufacturer=command.dto.manufacturer,
            category=command.dto.category,
            status=command.dto.status,
            purchase_date=command.dto.purchase_date,
            warranty_end_date=command.dto.warranty_end_date,
            location=command.dto.location,
            specifications=command.dto.specifications,
            tags=command.dto.tags
        )
        return await self.repository.create(equipment) 