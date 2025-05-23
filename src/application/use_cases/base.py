from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Any

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")
T = TypeVar('T')

class BaseUseCase(ABC, Generic[InputType, OutputType]):
    @abstractmethod
    async def execute(self, input_data: Optional[InputType] = None) -> OutputType:
        pass 

class Command(ABC):
    """Base class for all commands. Commands are handled by CommandHandlers."""
    pass

class Query(ABC):
    """Base class for all queries. Queries are handled by QueryHandlers."""
    pass

class CommandHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, command: T) -> Any:
        pass

class QueryHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, query: T) -> Any:
        pass 