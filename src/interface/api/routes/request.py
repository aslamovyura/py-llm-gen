from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from src.application.use_cases.request.queries.get_request import GetRequestQuery, GetRequestHandler
from src.application.use_cases.request.queries.list_requests import ListRequestsQuery, ListRequestsHandler
from src.application.use_cases.request.commands.create_request import CreateRequestCommand, CreateRequestHandler
from src.application.use_cases.request.commands.update_request import UpdateRequestCommand, UpdateRequestHandler
from src.application.use_cases.request.commands.delete_request import DeleteRequestCommand, DeleteRequestHandler
from src.domain.entities.request import Request
from src.application.dto.request import RequestCreateDTO, RequestUpdateDTO
from src.interface.api.dependencies import resolve_handler

router = APIRouter(prefix="/requests", tags=["requests"])

@router.get("/", response_model=List[Request])
async def list_requests(
    handler: ListRequestsHandler = Depends(resolve_handler(ListRequestsHandler))
):
    query = ListRequestsQuery()
    requests = await handler.handle(query)
    return requests

@router.get("/{request_id}", response_model=Request)
async def get_request(
    request_id: str,
    handler: GetRequestHandler = Depends(resolve_handler(GetRequestHandler))
):
    query = GetRequestQuery(request_id=request_id)
    request = await handler.handle(query)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.post("/", response_model=Request, status_code=201)
async def create_request(
    request_data: RequestCreateDTO,
    handler: CreateRequestHandler = Depends(resolve_handler(CreateRequestHandler))
):
    command = CreateRequestCommand(dto=request_data)
    request = await handler.handle(command)
    return request

@router.put("/{request_id}", response_model=Request)
async def update_request(
    request_id: str,
    request_data: RequestUpdateDTO,
    handler: UpdateRequestHandler = Depends(resolve_handler(UpdateRequestHandler))
):
    command = UpdateRequestCommand(request_id=request_id, dto=request_data)
    request = await handler.handle(command)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.delete("/{request_id}", status_code=204)
async def delete_request(
    request_id: str,
    handler: DeleteRequestHandler = Depends(resolve_handler(DeleteRequestHandler))
):
    command = DeleteRequestCommand(request_id=request_id)
    await handler.handle(command) 