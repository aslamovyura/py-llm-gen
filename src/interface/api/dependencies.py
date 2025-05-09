from typing import Type, TypeVar, Callable, Any, Dict, cast
from inspect import isclass

from src.infrastructure.di.container import container
from src.application.use_cases.base import QueryHandler, CommandHandler

# Type variables for generic handler factory functions
T = TypeVar('T')
H = TypeVar('H')

# Get repository for a handler based on class name
def get_repository_for_handler(handler_class_name: str):
    repo_factory = container.repository_factory
    
    if "Client" in handler_class_name:
        return repo_factory.get_client_repository()
    elif "User" in handler_class_name:
        return repo_factory.get_user_repository()
    elif "Offer" in handler_class_name:
        return repo_factory.get_offer_repository()
    elif "Request" in handler_class_name:
        return repo_factory.get_request_repository()
    elif "Equipment" in handler_class_name:
        return repo_factory.get_equipment_repository()
    else:
        raise ValueError(f"Unknown handler type: {handler_class_name}")

# Generic factory function for any handler
async def resolve_handler(handler_cls: Type[H]) -> H:
    """
    FastAPI dependency that creates and returns a handler instance with 
    the appropriate repository dependency.
    """
    try:
        # Get the appropriate repository
        repo = get_repository_for_handler(handler_cls.__name__)
        
        # Create and return the handler
        return handler_cls(repository=repo)
    except Exception as e:
        # Provide a more helpful error message
        class_name = handler_cls.__name__ if isclass(handler_cls) else str(handler_cls)
        raise RuntimeError(f"Failed to resolve handler {class_name}: {str(e)}") from e 