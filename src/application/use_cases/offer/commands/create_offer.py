from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....dto.offer import CreateOfferDTO
from ....repositories.offer import OfferRepository
from ....entities.offer import Offer

@dataclass
class CreateOfferCommand(Command):
    dto: CreateOfferDTO

class CreateOfferHandler(CommandHandler[CreateOfferCommand]):
    def __init__(self, repository: OfferRepository):
        self.repository = repository

    async def handle(self, command: CreateOfferCommand) -> Offer:
        offer = Offer(
            request_id=command.dto.request_id,
            equipment_id=command.dto.equipment_id,
            price=command.dto.price,
            currency=command.dto.currency,
            quantity=command.dto.quantity,
            delivery_date=command.dto.delivery_date,
            warranty_period_months=command.dto.warranty_period_months,
            status=command.dto.status,
            terms_and_conditions=command.dto.terms_and_conditions,
            notes=command.dto.notes,
            additional_services=command.dto.additional_services,
            discount_percentage=command.dto.discount_percentage,
            payment_terms=command.dto.payment_terms,
            custom_payment_terms=command.dto.custom_payment_terms
        )
        return await self.repository.create(offer) 