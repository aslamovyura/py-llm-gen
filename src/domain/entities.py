from dataclasses import dataclass
from datetime import datetime

@dataclass
class Deal:
    id: int
    title: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime 