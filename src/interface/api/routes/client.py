from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.application.use_cases.client.queries.get_client import GetClientQuery, GetClientHandler
from src.application.use_cases.client.queries.list_clients import ListClientsQuery, ListClientsHandler
from src.application.use_cases.client.commands.create_client import CreateClientCommand, CreateClientHandler
from src.application.use_cases.client.commands.update_client import UpdateClientCommand, UpdateClientHandler
from src.application.use_cases.client.commands.delete_client import DeleteClientCommand, DeleteClientHandler
from src.domain.entities.client import Client
from src.application.dto.client import ClientCreateDTO, ClientUpdateDTO
from src.interface.api.dependencies import resolve_handler

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=List[Client])
async def list_clients(
    handler: ListClientsHandler = Depends(resolve_handler(ListClientsHandler))
):
    query = ListClientsQuery()
    clients = await handler.handle(query)
    return clients

@router.get("/{client_id}", response_model=Client)
async def get_client(
    client_id: str,
    handler: GetClientHandler = Depends(resolve_handler(GetClientHandler))
):
    query = GetClientQuery(client_id=client_id)
    client = await handler.handle(query)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/", response_model=Client, status_code=201)
async def create_client(
    client_data: ClientCreateDTO,
    handler: CreateClientHandler = Depends(resolve_handler(CreateClientHandler))
):
    command = CreateClientCommand(dto=client_data)
    client = await handler.handle(command)
    return client

@router.put("/{client_id}", response_model=Client)
async def update_client(
    client_id: str,
    client_data: ClientUpdateDTO,
    handler: UpdateClientHandler = Depends(resolve_handler(UpdateClientHandler))
):
    command = UpdateClientCommand(client_id=client_id, dto=client_data)
    client = await handler.handle(command)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.delete("/{client_id}", status_code=204)
async def delete_client(
    client_id: str,
    handler: DeleteClientHandler = Depends(resolve_handler(DeleteClientHandler))
):
    command = DeleteClientCommand(client_id=client_id)
    await handler.handle(command) 