from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dictionaries import RolesDict
from app.models.settings import RoleFunction


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[RolesDict]:
        result = await self.session.execute(
            select(RolesDict),
        )
        return list(result.scalars().all())

    async def get_by_id(
        self, role_id: int,
    ) -> RolesDict | None:
        result = await self.session.execute(
            select(RolesDict).where(
                RolesDict.id == role_id,
            ),
        )
        return result.scalar_one_or_none()

    async def get_functions(
        self, role_id: int,
    ) -> list[RoleFunction]:
        result = await self.session.execute(
            select(RoleFunction).where(
                RoleFunction.role_id == role_id,
            ),
        )
        return list(result.scalars().all())

    async def get_function_link(
        self, role_id: int, function_id: int,
    ) -> RoleFunction | None:
        result = await self.session.execute(
            select(RoleFunction).where(
                RoleFunction.role_id == role_id,
                RoleFunction.function_code_id
                == function_id,
            ),
        )
        return result.scalar_one_or_none()

    async def add_function(
        self, role_function: RoleFunction,
    ) -> RoleFunction:
        try:
            self.session.add(role_function)
            await self.session.commit()
            await self.session.refresh(role_function)
            return role_function
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Function already assigned "
                "or invalid reference",
            )

    async def remove_function(
        self, role_function: RoleFunction,
    ) -> None:
        await self.session.delete(role_function)
        await self.session.commit()
