from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....repositories.equipment import EquipmentRepository

@dataclass
class DeleteEquipmentCommand(Command):
    equipment_id: str

class DeleteEquipmentHandler(CommandHandler[DeleteEquipmentCommand]):
    def __init__(self, repository: EquipmentRepository):
        self.repository = repository

    async def handle(self, command: DeleteEquipmentCommand) -> bool:
        return await self.repository.delete(command.equipment_id) 