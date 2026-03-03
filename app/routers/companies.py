from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import (
    get_own_company_or_superuser, get_superuser,
)
from app.cache import CachedUser
from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


def get_service(session: AsyncSession = Depends(get_db)) -> CompanyService:
    return CompanyService(session)


@router.post(
    "/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED,
)
async def create_company(
    data: CompanyCreate,
    service: CompanyService = Depends(get_service),
):
    """Публичный endpoint: регистрация компании."""
    return await service.create_company(data)


@router.get("/", response_model=list[CompanyResponse])
async def list_companies(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: CompanyService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    return await service.get_companies(offset=offset, limit=limit)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    service: CompanyService = Depends(get_service),
    _: CachedUser = Depends(get_own_company_or_superuser),
):
    return await service.get_company(company_id)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    data: CompanyUpdate,
    service: CompanyService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    return await service.update_company(company_id, data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    service: CompanyService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    await service.delete_company(company_id)
