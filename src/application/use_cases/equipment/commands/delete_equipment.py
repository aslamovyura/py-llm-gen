from dataclasses import dataclass

from src.infrastructure.repositories.equipment import EquipmentRepository
from ...base import Command, CommandHandler


@dataclass
class DeleteEquipmentCommand(Command):
    equipment_id: int

class DeleteEquipmentHandler(CommandHandler[DeleteEquipmentCommand]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, command: DeleteEquipmentCommand) -> bool:
        return await self.repository.delete(command.equipment_id) 