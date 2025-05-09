from dataclasses import dataclass
from typing import Optional, Dict, List
from ...base import Command, CommandHandler
from src.application.dto.equipment import EquipmentUpdateDTO
from src.infrastructure.repositories.equipment import EquipmentRepository
from src.domain.entities.equipment import Equipment

@dataclass
class UpdateEquipmentCommand(Command):
    equipment_id: int
    dto: EquipmentUpdateDTO

class UpdateEquipmentHandler(CommandHandler[UpdateEquipmentCommand]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, command: UpdateEquipmentCommand) -> Optional[Equipment]:
        equipment = await self.repository.get_by_id(command.equipment_id)
        if not equipment:
            return None

        update_data = command.dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(equipment, field, value)

        return await self.repository.update(equipment) 