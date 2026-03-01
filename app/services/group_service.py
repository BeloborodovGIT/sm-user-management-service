from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserGroup
from app.repositories.group_repository import GroupRepository
from app.schemas.group import GroupCreate, GroupUpdate


class GroupService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = GroupRepository(session)

    async def get_group(self, group_id: int) -> UserGroup:
        group = await self.repo.get_by_id(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
            )
        return group

    async def get_groups(
        self, company_id: int | None = None, offset: int = 0, limit: int = 100
    ) -> list[UserGroup]:
        return await self.repo.get_all(
            company_id=company_id, offset=offset, limit=limit
        )

    async def create_group(self, data: GroupCreate) -> UserGroup:
        group = UserGroup(
            company_id=data.company_id,
            group_name=data.group_name,
            comment=data.comment,
        )
        return await self.repo.create(group)

    async def update_group(self, group_id: int, data: GroupUpdate) -> UserGroup:
        group = await self.get_group(group_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(group, field, value)
        return await self.repo.update(group)

    async def delete_group(self, group_id: int) -> None:
        group = await self.get_group(group_id)
        await self.repo.delete(group)
