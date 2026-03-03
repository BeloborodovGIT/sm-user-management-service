from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_superuser
from app.cache import CachedUser
from app.database import get_db
from app.schemas.setting import SettingCreate, SettingResponse, SettingUpdate
from app.services.setting_service import SettingService

router = APIRouter(prefix="/settings", tags=["settings"])


def get_service(session: AsyncSession = Depends(get_db)) -> SettingService:
    return SettingService(session)


@router.get("/", response_model=list[SettingResponse])
async def list_settings(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: SettingService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    return await service.get_settings(
        offset=offset, limit=limit,
    )


@router.post(
    "/",
    response_model=SettingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_setting(
    data: SettingCreate,
    service: SettingService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    return await service.create_setting(data)


@router.get("/{setting_id}", response_model=SettingResponse)
async def get_setting(
    setting_id: int,
    service: SettingService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    return await service.get_setting(setting_id)


@router.patch("/{setting_id}", response_model=SettingResponse)
async def update_setting(
    setting_id: int,
    data: SettingUpdate,
    service: SettingService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    return await service.update_setting(setting_id, data)


@router.delete("/{setting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(
    setting_id: int,
    service: SettingService = Depends(get_service),
    _: CachedUser = Depends(get_superuser),
):
    await service.delete_setting(setting_id)
