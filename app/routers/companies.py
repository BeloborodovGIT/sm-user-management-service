from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


def get_service(session: AsyncSession = Depends(get_db)) -> CompanyService:
    return CompanyService(session)


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompanyCreate,
    service: CompanyService = Depends(get_service),
):
    """Публичный endpoint: регистрация компании."""
    return await service.create_company(data)


@router.get("/", response_model=list[CompanyResponse])
async def list_companies(
    offset: int = 0,
    limit: int = 100,
    service: CompanyService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.get_companies(offset=offset, limit=limit)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    service: CompanyService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.get_company(company_id)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    data: CompanyUpdate,
    service: CompanyService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.update_company(company_id, data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    service: CompanyService = Depends(get_service),
    _=Depends(get_current_user),
):
    await service.delete_company(company_id)
