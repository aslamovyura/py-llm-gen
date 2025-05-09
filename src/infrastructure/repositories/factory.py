from typing import Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories.base import BaseRepository
from .user import UserRepository
from .client import ClientRepository
from .request import RequestRepository
from .offer import OfferRepository
from .equipment import EquipmentRepository

class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._repositories: Dict[Type[BaseRepository], BaseRepository] = {}

    def get_user_repository(self) -> UserRepository:
        if UserRepository not in self._repositories:
            self._repositories[UserRepository] = UserRepository(self.session)
        return self._repositories[UserRepository]

    def get_client_repository(self) -> ClientRepository:
        if ClientRepository not in self._repositories:
            self._repositories[ClientRepository] = ClientRepository(self.session)
        return self._repositories[ClientRepository]

    def get_request_repository(self) -> RequestRepository:
        if RequestRepository not in self._repositories:
            self._repositories[RequestRepository] = RequestRepository(self.session)
        return self._repositories[RequestRepository]

    def get_offer_repository(self) -> OfferRepository:
        if OfferRepository not in self._repositories:
            self._repositories[OfferRepository] = OfferRepository(self.session)
        return self._repositories[OfferRepository]

    def get_equipment_repository(self) -> EquipmentRepository:
        if EquipmentRepository not in self._repositories:
            self._repositories[EquipmentRepository] = EquipmentRepository(self.session)
        return self._repositories[EquipmentRepository] 