from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")

class BaseUseCase(ABC, Generic[InputType, OutputType]):
    @abstractmethod
    async def execute(self, input_data: Optional[InputType] = None) -> OutputType:
        pass 