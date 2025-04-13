from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from src.application.use_cases.equipment.queries.get_equipment import GetEquipmentQuery, GetEquipmentHandler
from src.application.use_cases.equipment.queries.list_equipment import ListEquipmentQuery, ListEquipmentHandler
from src.application.use_cases.equipment.commands.create_equipment import CreateEquipmentCommand, CreateEquipmentHandler
from src.application.use_cases.equipment.commands.update_equipment import UpdateEquipmentCommand, UpdateEquipmentHandler
from src.application.use_cases.equipment.commands.delete_equipment import DeleteEquipmentCommand, DeleteEquipmentHandler
from src.domain.entities.equipment import Equipment
from src.application.dto.equipment import EquipmentCreateDTO, EquipmentUpdateDTO
from src.infrastructure.di.container import Container

router = APIRouter(prefix="/equipment", tags=["equipment"])

@router.get("/", response_model=List[Equipment])
async def list_equipment(
    handler: ListEquipmentHandler = Depends(Container.resolve(ListEquipmentHandler))
):
    query = ListEquipmentQuery()
    equipment = await handler.handle(query)
    return equipment

@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment(
    equipment_id: str,
    handler: GetEquipmentHandler = Depends(Container.resolve(GetEquipmentHandler))
):
    query = GetEquipmentQuery(equipment_id=equipment_id)
    equipment = await handler.handle(query)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.post("/", response_model=Equipment, status_code=201)
async def create_equipment(
    equipment_data: EquipmentCreateDTO,
    handler: CreateEquipmentHandler = Depends(Container.resolve(CreateEquipmentHandler))
):
    command = CreateEquipmentCommand(**equipment_data.dict())
    equipment = await handler.handle(command)
    return equipment

@router.put("/{equipment_id}", response_model=Equipment)
async def update_equipment(
    equipment_id: str,
    equipment_data: EquipmentUpdateDTO,
    handler: UpdateEquipmentHandler = Depends(Container.resolve(UpdateEquipmentHandler))
):
    command = UpdateEquipmentCommand(equipment_id=equipment_id, **equipment_data.dict())
    equipment = await handler.handle(command)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.delete("/{equipment_id}", status_code=204)
async def delete_equipment(
    equipment_id: str,
    handler: DeleteEquipmentHandler = Depends(Container.resolve(DeleteEquipmentHandler))
):
    command = DeleteEquipmentCommand(equipment_id=equipment_id)
    await handler.handle(command) 