from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.schemas.group import GroupCreate, GroupResponse, GroupUpdate
from app.services.group_service import GroupService

router = APIRouter(prefix="/groups", tags=["groups"])


def get_service(session: AsyncSession = Depends(get_db)) -> GroupService:
    return GroupService(session)


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    data: GroupCreate,
    service: GroupService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.create_group(data)


@router.get("/", response_model=list[GroupResponse])
async def list_groups(
    company_id: int | None = None,
    offset: int = 0,
    limit: int = 100,
    service: GroupService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.get_groups(company_id=company_id, offset=offset, limit=limit)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    service: GroupService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.get_group(group_id)


@router.patch("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    data: GroupUpdate,
    service: GroupService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.update_group(group_id, data)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    service: GroupService = Depends(get_service),
    _=Depends(get_current_user),
):
    await service.delete_group(group_id)
