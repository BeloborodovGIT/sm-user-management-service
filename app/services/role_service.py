from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import (
    get_cached_dict,
    invalidate_dict,
    set_cached_dict,
)
from app.models.dictionaries import RolesDict
from app.models.settings import RoleFunction
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleFunctionCreate

_ROLES_CACHE_KEY = "all_roles"


class RoleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = RoleRepository(session)

    async def get_roles(self) -> list[RolesDict]:
        cached = await get_cached_dict(_ROLES_CACHE_KEY)
        if cached is not None:
            return cached
        roles = await self.repo.get_all()
        await set_cached_dict(_ROLES_CACHE_KEY, roles)
        return roles

    async def get_role(self, role_id: int) -> RolesDict:
        role = await self.repo.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            )
        return role

    async def get_role_functions(self, role_id: int) -> list[RoleFunction]:
        await self.get_role(role_id)
        return await self.repo.get_functions(role_id)

    async def add_function(self, role_id: int, data: RoleFunctionCreate) -> RoleFunction:
        await self.get_role(role_id)
        existing = await self.repo.get_function_link(role_id, data.function_code_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Function already assigned to role",
            )
        role_function = RoleFunction(
            role_id=role_id,
            function_code_id=data.function_code_id,
        )
        result = await self.repo.add_function(role_function)
        await invalidate_dict(_ROLES_CACHE_KEY)
        return result

    async def remove_function(self, role_id: int, function_id: int) -> None:
        link = await self.repo.get_function_link(role_id, function_id)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Function not assigned to role",
            )
        await self.repo.remove_function(link)
        await invalidate_dict(_ROLES_CACHE_KEY)
