from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from src.application.use_cases.user.queries.get_user import GetUserQuery, GetUserHandler
from src.application.use_cases.user.queries.get_user_by_username import GetUserByUsernameQuery, GetUserByUsernameHandler
from src.application.use_cases.user.queries.list_users import ListUsersQuery, ListUsersHandler
from src.application.use_cases.user.commands.create_user import CreateUserCommand, CreateUserHandler
from src.application.use_cases.user.commands.update_user import UpdateUserCommand, UpdateUserHandler
from src.application.use_cases.user.commands.delete_user import DeleteUserCommand, DeleteUserHandler
from src.domain.entities.user import User
from src.application.dto.user import UserCreateDTO, UserUpdateDTO
from src.infrastructure.di.container import Container

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
async def list_users(
    handler: ListUsersHandler = Depends(Container.resolve(ListUsersHandler))
):
    query = ListUsersQuery()
    users = await handler.handle(query)
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    handler: GetUserHandler = Depends(Container.resolve(GetUserHandler))
):
    query = GetUserQuery(user_id=user_id)
    user = await handler.handle(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/username/{username}", response_model=User)
async def get_user_by_username(
    username: str,
    handler: GetUserByUsernameHandler = Depends(Container.resolve(GetUserByUsernameHandler))
):
    query = GetUserByUsernameQuery(username=username)
    user = await handler.handle(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User, status_code=201)
async def create_user(
    user_data: UserCreateDTO,
    handler: CreateUserHandler = Depends(Container.resolve(CreateUserHandler))
):
    command = CreateUserCommand(**user_data.dict())
    user = await handler.handle(command)
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_data: UserUpdateDTO,
    handler: UpdateUserHandler = Depends(Container.resolve(UpdateUserHandler))
):
    command = UpdateUserCommand(user_id=user_id, **user_data.dict())
    user = await handler.handle(command)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    handler: DeleteUserHandler = Depends(Container.resolve(DeleteUserHandler))
):
    command = DeleteUserCommand(user_id=user_id)
    await handler.handle(command) 