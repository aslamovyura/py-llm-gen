from typing import Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories.base import BaseRepository
from .user import UserSQLRepository
from .client import ClientSQLRepository
from .request import RequestSQLRepository
from .offer import OfferSQLRepository
from .equipment import EquipmentSQLRepository

class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._repositories: Dict[Type[BaseRepository], BaseRepository] = {}

    def get_user_repository(self) -> UserSQLRepository:
        if UserSQLRepository not in self._repositories:
            self._repositories[UserSQLRepository] = UserSQLRepository(self.session)
        return self._repositories[UserSQLRepository]

    def get_client_repository(self) -> ClientSQLRepository:
        if ClientSQLRepository not in self._repositories:
            self._repositories[ClientSQLRepository] = ClientSQLRepository(self.session)
        return self._repositories[ClientSQLRepository]

    def get_request_repository(self) -> RequestSQLRepository:
        if RequestSQLRepository not in self._repositories:
            self._repositories[RequestSQLRepository] = RequestSQLRepository(self.session)
        return self._repositories[RequestSQLRepository]

    def get_offer_repository(self) -> OfferSQLRepository:
        if OfferSQLRepository not in self._repositories:
            self._repositories[OfferSQLRepository] = OfferSQLRepository(self.session)
        return self._repositories[OfferSQLRepository]

    def get_equipment_repository(self) -> EquipmentSQLRepository:
        if EquipmentSQLRepository not in self._repositories:
            self._repositories[EquipmentSQLRepository] = EquipmentSQLRepository(self.session)
        return self._repositories[EquipmentSQLRepository] 