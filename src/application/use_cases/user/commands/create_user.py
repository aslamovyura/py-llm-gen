from dataclasses import dataclass
from ...base import Command, CommandHandler
from src.application.dto.user import UserCreateDTO
from src.infrastructure.repositories.user import UserRepository
from src.domain.entities.user import User

@dataclass
class CreateUserCommand(Command):
    dto: UserCreateDTO

class CreateUserHandler(CommandHandler[CreateUserCommand]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, command: CreateUserCommand) -> User:
        user_entity = User(
            username=command.dto.username,
            email=command.dto.email,
            full_name=command.dto.full_name,
            hashed_password=command.dto.hashed_password,
            role=command.dto.role,
            phone_number=command.dto.phone_number
        )
        return await self.repository.create(user_entity) 