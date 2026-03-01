from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import (
    _user_has_superuser_role,
    get_self_or_superuser,
    get_superuser,
)
from app.database import get_db
from app.models.user import User
from app.schemas.role import UserRoleCreate, UserRoleResponse
from app.schemas.user import UserRegister, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

SELF_EDIT_RESTRICTED_FIELDS = {
    "user_lock", "group_id", "company_id", "timezone_id",
}


def get_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: UserRegister,
    service: UserService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.register(data)


@router.get("/", response_model=list[UserResponse])
async def list_users(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: UserService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.get_users(offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_service),
    _: User = Depends(get_self_or_superuser),
):
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_service),
    current_user: User = Depends(get_self_or_superuser),
    session: AsyncSession = Depends(get_db),
):
    # Regular users cannot change privileged fields on themselves
    if not await _user_has_superuser_role(current_user.id, session):
        update_data = data.model_dump(exclude_unset=True)
        for field in SELF_EDIT_RESTRICTED_FIELDS:
            update_data.pop(field, None)
        data = UserUpdate(**update_data)
    return await service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    await service.delete_user(user_id)


@router.get("/{user_id}/roles", response_model=list[UserRoleResponse])
async def get_user_roles(
    user_id: int,
    service: UserService = Depends(get_service),
    _: User = Depends(get_self_or_superuser),
):
    return await service.get_roles(user_id)


@router.post(
    "/{user_id}/roles",
    response_model=UserRoleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def assign_role(
    user_id: int,
    data: UserRoleCreate,
    service: UserService = Depends(get_service),
    _: User = Depends(get_superuser),
):
    return await service.assign_role(user_id, data)
