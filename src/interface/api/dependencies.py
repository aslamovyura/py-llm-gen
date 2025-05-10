from typing import Type, TypeVar, Callable, Any, Dict, cast
from inspect import isclass
from functools import partial

from src.infrastructure.di.container import container
from src.application.use_cases.base import QueryHandler, CommandHandler
from src.infrastructure.di.dependencies import inject_repository

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

# Create a factory function for a specific handler class
def create_handler_factory(handler_cls: Type[H]) -> Callable[[], H]:
    """
    Creates a factory function that will instantiate the handler with its repository.
    This is what FastAPI's Depends() expects.
    """
    def factory() -> H:
        try:
            # Get the appropriate repository
            repo = get_repository_for_handler(handler_cls.__name__)
            
            # Create and return the handler
            return handler_cls(repository=repo)
        except Exception as e:
            # Provide a more helpful error message
            class_name = handler_cls.__name__ if isclass(handler_cls) else str(handler_cls)
            raise RuntimeError(f"Failed to resolve handler {class_name}: {str(e)}") from e
    
    return factory

# Main resolver function that FastAPI will use
def resolve_handler(handler_class: Type[T]) -> Callable[[], T]:
    """
    Creates a factory function that will instantiate a handler with its required repository.
    """
    def factory() -> T:
        try:
            # Get the appropriate repository based on handler class name
            repo = get_repository_for_handler(handler_class.__name__)
            
            # Create and return the handler with the repository
            return handler_class(repository=repo)
            
        except Exception as e:
            class_name = handler_class.__name__
            raise RuntimeError(f"Failed to resolve handler {class_name}: {str(e)}") from e
    
    return factory

# Handler provider functions
def get_list_clients_handler():
    from src.application.use_cases.client.queries.list_clients import ListClientsHandler
    return resolve_handler(ListClientsHandler)()

def get_get_client_handler():
    from src.application.use_cases.client.queries.get_client import GetClientHandler
    return resolve_handler(GetClientHandler)()

def get_create_client_handler():
    from src.application.use_cases.client.commands.create_client import CreateClientHandler
    return resolve_handler(CreateClientHandler)()

def get_update_client_handler():
    from src.application.use_cases.client.commands.update_client import UpdateClientHandler
    return resolve_handler(UpdateClientHandler)()

def get_delete_client_handler():
    from src.application.use_cases.client.commands.delete_client import DeleteClientHandler
    return resolve_handler(DeleteClientHandler)()

def get_list_users_handler():
    from src.application.use_cases.user.queries.list_users import ListUsersHandler
    return resolve_handler(ListUsersHandler)()

def get_get_user_handler():
    from src.application.use_cases.user.queries.get_user import GetUserHandler
    return resolve_handler(GetUserHandler)()

def get_get_user_by_username_handler():
    from src.application.use_cases.user.queries.get_user_by_username import GetUserByUsernameHandler
    return resolve_handler(GetUserByUsernameHandler)()

def get_create_user_handler():
    from src.application.use_cases.user.commands.create_user import CreateUserHandler
    return resolve_handler(CreateUserHandler)()

def get_update_user_handler():
    from src.application.use_cases.user.commands.update_user import UpdateUserHandler
    return resolve_handler(UpdateUserHandler)()

def get_delete_user_handler():
    from src.application.use_cases.user.commands.delete_user import DeleteUserHandler
    return resolve_handler(DeleteUserHandler)()

def get_list_offers_handler():
    from src.application.use_cases.offer.queries.list_offers import ListOffersHandler
    return resolve_handler(ListOffersHandler)()

def get_get_offer_handler():
    from src.application.use_cases.offer.queries.get_offer import GetOfferHandler
    return resolve_handler(GetOfferHandler)()

def get_create_offer_handler():
    from src.application.use_cases.offer.commands.create_offer import CreateOfferHandler
    return resolve_handler(CreateOfferHandler)()

def get_update_offer_handler():
    from src.application.use_cases.offer.commands.update_offer import UpdateOfferHandler
    return resolve_handler(UpdateOfferHandler)()

def get_delete_offer_handler():
    from src.application.use_cases.offer.commands.delete_offer import DeleteOfferHandler
    return resolve_handler(DeleteOfferHandler)()

def get_list_requests_handler():
    from src.application.use_cases.request.queries.list_requests import ListRequestsHandler
    return resolve_handler(ListRequestsHandler)()

def get_get_request_handler():
    from src.application.use_cases.request.queries.get_request import GetRequestHandler
    return resolve_handler(GetRequestHandler)()

def get_create_request_handler():
    from src.application.use_cases.request.commands.create_request import CreateRequestHandler
    return resolve_handler(CreateRequestHandler)()

def get_update_request_handler():
    from src.application.use_cases.request.commands.update_request import UpdateRequestHandler
    return resolve_handler(UpdateRequestHandler)()

def get_delete_request_handler():
    from src.application.use_cases.request.commands.delete_request import DeleteRequestHandler
    return resolve_handler(DeleteRequestHandler)()

def get_list_equipment_handler():
    from src.application.use_cases.equipment.queries.list_equipment import ListEquipmentHandler
    return resolve_handler(ListEquipmentHandler)()

def get_get_equipment_handler():
    from src.application.use_cases.equipment.queries.get_equipment import GetEquipmentHandler
    return resolve_handler(GetEquipmentHandler)()

def get_create_equipment_handler():
    from src.application.use_cases.equipment.commands.create_equipment import CreateEquipmentHandler
    return resolve_handler(CreateEquipmentHandler)()

def get_update_equipment_handler():
    from src.application.use_cases.equipment.commands.update_equipment import UpdateEquipmentHandler
    return resolve_handler(UpdateEquipmentHandler)()

def get_delete_equipment_handler():
    from src.application.use_cases.equipment.commands.delete_equipment import DeleteEquipmentHandler
    return resolve_handler(DeleteEquipmentHandler)() 