from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_superuser
from app.database import get_db
from app.models.user import User
from app.schemas.role import (
    RoleFunctionCreate, RoleFunctionResponse, RoleResponse,
)
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


def get_service(session: AsyncSession = Depends(get_db)) -> RoleService:
    return RoleService(session)


@router.get("/", response_model=list[RoleResponse])
async def list_roles(
    service: RoleService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.get_roles()


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    service: RoleService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.get_role(role_id)


@router.get("/{role_id}/functions", response_model=list[RoleFunctionResponse])
async def get_role_functions(
    role_id: int,
    service: RoleService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.get_role_functions(role_id)


@router.post(
    "/{role_id}/functions",
    response_model=RoleFunctionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_function_to_role(
    role_id: int,
    data: RoleFunctionCreate,
    service: RoleService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.add_function(role_id, data)


@router.delete(
    "/{role_id}/functions/{function_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_function_from_role(
    role_id: int,
    function_id: int,
    service: RoleService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    await service.remove_function(role_id, function_id)
