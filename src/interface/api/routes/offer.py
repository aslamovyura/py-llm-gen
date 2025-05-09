from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from src.application.use_cases.offer.queries.get_offer import GetOfferQuery, GetOfferHandler
from src.application.use_cases.offer.queries.list_offers import ListOffersQuery, ListOffersHandler
from src.application.use_cases.offer.commands.create_offer import CreateOfferCommand, CreateOfferHandler
from src.application.use_cases.offer.commands.update_offer import UpdateOfferCommand, UpdateOfferHandler
from src.application.use_cases.offer.commands.delete_offer import DeleteOfferCommand, DeleteOfferHandler
from src.domain.entities.offer import Offer
from src.application.dto.offer import OfferCreateDTO, OfferUpdateDTO
from src.interface.api.dependencies import resolve_handler

router = APIRouter(prefix="/offers", tags=["offers"])

@router.get("/", response_model=List[Offer])
async def list_offers(
    handler: ListOffersHandler = Depends(resolve_handler(ListOffersHandler))
):
    query = ListOffersQuery()
    offers = await handler.handle(query)
    return offers

@router.get("/{offer_id}", response_model=Offer)
async def get_offer(
    offer_id: str,
    handler: GetOfferHandler = Depends(resolve_handler(GetOfferHandler))
):
    query = GetOfferQuery(offer_id=offer_id)
    offer = await handler.handle(query)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.post("/", response_model=Offer, status_code=201)
async def create_offer(
    offer_data: OfferCreateDTO,
    handler: CreateOfferHandler = Depends(resolve_handler(CreateOfferHandler))
):
    command = CreateOfferCommand(dto=offer_data)
    offer = await handler.handle(command)
    return offer

@router.put("/{offer_id}", response_model=Offer)
async def update_offer(
    offer_id: str,
    offer_data: OfferUpdateDTO,
    handler: UpdateOfferHandler = Depends(resolve_handler(UpdateOfferHandler))
):
    command = UpdateOfferCommand(offer_id=offer_id, dto=offer_data)
    offer = await handler.handle(command)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.delete("/{offer_id}", status_code=204)
async def delete_offer(
    offer_id: str,
    handler: DeleteOfferHandler = Depends(resolve_handler(DeleteOfferHandler))
):
    command = DeleteOfferCommand(offer_id=offer_id)
    await handler.handle(command) 