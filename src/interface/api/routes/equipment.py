from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List, Optional
from src.application.use_cases.equipment.queries.get_equipment import GetEquipmentQuery, GetEquipmentHandler
from src.application.use_cases.equipment.queries.list_equipment import ListEquipmentQuery, ListEquipmentHandler
from src.application.use_cases.equipment.commands.create_equipment import CreateEquipmentCommand, CreateEquipmentHandler
from src.application.use_cases.equipment.commands.update_equipment import UpdateEquipmentCommand, UpdateEquipmentHandler
from src.application.use_cases.equipment.commands.delete_equipment import DeleteEquipmentCommand, DeleteEquipmentHandler
from src.domain.entities.equipment import Equipment
from src.application.dto.equipment import EquipmentCreateDTO, EquipmentUpdateDTO
from src.interface.api.dependencies import resolve_handler

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.get("/", response_model=List[Equipment])
async def list_equipment(
    handler: ListEquipmentHandler = Depends(resolve_handler(ListEquipmentHandler))
):
    query = ListEquipmentQuery()
    equipment = await handler.handle(query)
    return equipment

@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment(
    equipment_id: int = Path(..., gt=0),
    handler: GetEquipmentHandler = Depends(resolve_handler(GetEquipmentHandler))
):
    query = GetEquipmentQuery(equipment_id=equipment_id)
    equipment = await handler.handle(query)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.post("/", response_model=Equipment, status_code=201)
async def create_equipment(
    equipment_data: EquipmentCreateDTO,
    handler: CreateEquipmentHandler = Depends(resolve_handler(CreateEquipmentHandler))
):
    command = CreateEquipmentCommand(dto=equipment_data)
    equipment = await handler.handle(command)
    return equipment

@router.put("/{equipment_id}", response_model=Equipment)
async def update_equipment(
    equipment_data: EquipmentUpdateDTO,
    equipment_id: int = Path(..., gt=0),
    handler: UpdateEquipmentHandler = Depends(resolve_handler(UpdateEquipmentHandler))
):
    command = UpdateEquipmentCommand(equipment_id=equipment_id, dto=equipment_data)
    equipment = await handler.handle(command)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.delete("/{equipment_id}", status_code=204)
async def delete_equipment(
    equipment_id: int = Path(..., gt=0),
    handler: DeleteEquipmentHandler = Depends(resolve_handler(DeleteEquipmentHandler))
):
    command = DeleteEquipmentCommand(equipment_id=equipment_id)
    await handler.handle(command) 