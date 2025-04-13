from dataclasses import dataclass
from typing import Optional
from ...base import Command, CommandHandler
from ....dto.offer import UpdateOfferDTO
from ....repositories.offer import OfferRepository
from ....entities.offer import Offer

@dataclass
class UpdateOfferCommand(Command):
    offer_id: str
    dto: UpdateOfferDTO

class UpdateOfferHandler(CommandHandler[UpdateOfferCommand]):
    def __init__(self, repository: OfferRepository):
        self.repository = repository

    async def handle(self, command: UpdateOfferCommand) -> Optional[Offer]:
        offer = await self.repository.get_by_id(command.offer_id)
        if not offer:
            return None

        update_data = command.dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(offer, field, value)

        return await self.repository.update(offer) 