from functools import wraps
from typing import Callable, TypeVar, Any
from src.infrastructure.di.container import container

T = TypeVar('T')

def inject_repository(repository_type: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            repository = getattr(container.repository_factory, f'get_{repository_type}_repository')()
            kwargs[repository_type] = repository
            return await func(*args, **kwargs)
        return wrapper
    return decorator 