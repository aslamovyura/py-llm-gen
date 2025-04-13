from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from ...base import Command, CommandHandler
from ....dto.equipment import CreateEquipmentDTO
from ....repositories.equipment import EquipmentRepository
from ....entities.equipment import Equipment

@dataclass
class CreateEquipmentCommand(Command):
    dto: CreateEquipmentDTO

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