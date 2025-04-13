from dataclasses import dataclass
from ...base import Command, CommandHandler
from ....dto.user import CreateUserDTO
from ....repositories.user import UserRepository
from ....entities.user import User
from src.infrastructure.di.dependencies import inject_repository

@dataclass
class CreateUserCommand(Command):
    dto: CreateUserDTO

class CreateUserHandler(CommandHandler[CreateUserCommand]):
    @inject_repository('user')
    async def handle(self, command: CreateUserCommand, user: UserRepository) -> User:
        user_entity = User(
            username=command.dto.username,
            email=command.dto.email,
            full_name=command.dto.full_name,
            hashed_password=command.dto.hashed_password,
            role=command.dto.role,
            phone_number=command.dto.phone_number
        )
        return await user.create(user_entity) 