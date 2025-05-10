from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.domain.entities.equipment import Equipment
from src.infrastructure.database.models import Equipment as EquipmentModel
from .base_sql import BaseSQLRepository

class EquipmentRepository(BaseSQLRepository[EquipmentModel, Equipment]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EquipmentModel)

    def _to_entity(self, db_obj: EquipmentModel) -> Equipment:
        return Equipment(
            id=str(db_obj.id),  # Convert integer ID to string
            name=db_obj.name,
            model=db_obj.model,
            serial_number=db_obj.serial_number,
            manufacturer=db_obj.manufacturer,
            category=db_obj.category,
            status=db_obj.status,
            purchase_date=db_obj.purchase_date,
            warranty_end_date=db_obj.warranty_end_date,
            location=db_obj.location,
            specifications=db_obj.specifications or {},
            tags=db_obj.tags or {}
        )

    async def get_by_id(self, equipment_id: str) -> Optional[Equipment]:
        try:
            equipment_id_int = int(equipment_id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == equipment_id_int)
        )
        db_obj = result.scalar_one_or_none()
        return self._to_entity(db_obj) if db_obj else None

    async def list(self, filters: Dict = None, skip: int = 0, limit: int = 100) -> List[Equipment]:
        query = select(self.model_class)
        
        if filters:
            for key, value in filters.items():
                if '__icontains' in key:
                    field = key.replace('__icontains', '')
                    query = query.filter(getattr(self.model_class, field).ilike(f'%{value}%'))
                else:
                    query = query.filter(getattr(self.model_class, key) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        db_models = result.scalars().all()
        return [self._to_entity(model) for model in db_models]

    async def create(self, entity: Equipment) -> Optional[Equipment]:
        try:
            # First check if equipment with this serial number already exists
            result = await self.session.execute(
                select(self.model_class).filter(self.model_class.serial_number == entity.serial_number)
            )
            existing = result.scalar_one_or_none()
            if existing:
                return None  # Return None if equipment with this serial number already exists

            db_obj = self.model_class(
                name=entity.name,
                model=entity.model,
                serial_number=entity.serial_number,
                manufacturer=entity.manufacturer,
                category=entity.category,
                status=entity.status,
                purchase_date=entity.purchase_date,
                warranty_end_date=entity.warranty_end_date,
                location=entity.location,
                specifications=entity.specifications,
                tags=entity.tags,
                is_active=entity.is_active
            )
            self.session.add(db_obj)
            await self.session.flush()
            return self._to_entity(db_obj)
        except IntegrityError:
            await self.session.rollback()
            return None

    async def update(self, entity: Equipment) -> Optional[Equipment]:
        if not entity.id:
            return None
        try:
            equipment_id_int = int(entity.id)  # Convert string ID to integer
        except ValueError:
            return None
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == equipment_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        update_data = entity.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        await self.session.flush()
        return self._to_entity(db_obj)

    async def delete(self, equipment_id: str) -> bool:
        try:
            equipment_id_int = int(equipment_id)  # Convert string ID to integer
        except ValueError:
            return False
            
        result = await self.session.execute(
            select(self.model_class).filter(self.model_class.id == equipment_id_int)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.flush()
        return True 