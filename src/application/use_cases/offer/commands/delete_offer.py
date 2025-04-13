from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....repositories.offer import OfferRepository

@dataclass
class DeleteOfferCommand(Command):
    offer_id: str

class DeleteOfferHandler(CommandHandler[DeleteOfferCommand]):
    def __init__(self, repository: OfferRepository):
        self.repository = repository

    async def handle(self, command: DeleteOfferCommand) -> bool:
        return await self.repository.delete(command.offer_id) 