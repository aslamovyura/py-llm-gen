from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from domain.entities import Deal

Base = declarative_base()

class DealModel(Base):
    __tablename__ = 'deals'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class SQLAlchemyDealRepository:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        
    def search(self, query: str) -> list[Deal]:
        session = self.Session()
        try:
            results = session.query(DealModel).filter(
                DealModel.title.ilike(f'%{query}%') |
                DealModel.description.ilike(f'%{query}%')
            ).all()
            return [self._to_entity(deal) for deal in results]
        finally:
            session.close()
            
    def _to_entity(self, model: DealModel) -> Deal:
        return Deal(
            id=model.id,
            title=model.title,
            description=model.description,
            price=model.price,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 