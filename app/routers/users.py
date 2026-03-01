from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.schemas.role import UserRoleCreate, UserRoleResponse
from app.schemas.user import UserRegister, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    data: UserRegister,
    service: UserService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.register(data)


@router.get("/", response_model=list[UserResponse])
async def list_users(
    offset: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.get_users(offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_service),
    _=Depends(get_current_user),
):
    return await service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_service),
    _=Depends(get_current_user),
):
    await service.delete_user(user_id)


@router.get("/{user_id}/roles", response_model=list[UserRoleResponse])
async def get_user_roles(
    user_id: int,
    service: UserService = Depends(get_service),
    _=Depends(get_current_user),
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
    _=Depends(get_current_user),
):
    return await service.assign_role(user_id, data)
