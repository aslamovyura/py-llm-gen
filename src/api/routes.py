from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel

from src.application.use_cases.search_deals import SearchDealsUseCase
from src.domain.entities.deal import Deal
from src.infrastructure.database.session import get_db_session

router = APIRouter()

class DealResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    created_at: str

    class Config:
        from_attributes = True

class SearchDealsRequest(BaseModel):
    query: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"

@router.post("/deals/search", response_model=List[DealResponse])
async def search_deals(
    request: SearchDealsRequest,
    db_session = Depends(get_db_session)
) -> List[DealResponse]:
    """
    Search for deals based on query parameters.
    """
    try:
        use_case = SearchDealsUseCase(db_session)
        deals = await use_case.execute(
            query=request.query,
            min_price=request.min_price,
            max_price=request.max_price,
            sort_by=request.sort_by,
            sort_order=request.sort_order
        )
        return [DealResponse.from_orm(deal) for deal in deals]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deals/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: int,
    db_session = Depends(get_db_session)
) -> DealResponse:
    """
    Get a specific deal by ID.
    """
    try:
        use_case = SearchDealsUseCase(db_session)
        deal = await use_case.get_by_id(deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        return DealResponse.from_orm(deal)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deals", response_model=List[DealResponse])
async def list_deals(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db_session = Depends(get_db_session)
) -> List[DealResponse]:
    """
    List all deals with pagination.
    """
    try:
        use_case = SearchDealsUseCase(db_session)
        deals = await use_case.list_deals(page=page, page_size=page_size)
        return [DealResponse.from_orm(deal) for deal in deals]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 