from dataclasses import dataclass
from typing import Optional
from ...base import Command, CommandHandler
from src.application.dto.offer import OfferUpdateDTO
from src.infrastructure.repositories.offer import OfferRepository
from src.domain.entities.offer import Offer

@dataclass
class UpdateOfferCommand(Command):
    offer_id: int
    dto: OfferUpdateDTO

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