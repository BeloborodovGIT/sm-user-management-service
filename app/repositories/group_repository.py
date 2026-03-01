from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserGroup


class GroupRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, group_id: int) -> UserGroup | None:
        result = await self.session.execute(
            select(UserGroup).where(UserGroup.id == group_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        company_id: int | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGroup]:
        query = select(UserGroup)
        if company_id is not None:
            query = query.where(UserGroup.company_id == company_id)
        result = await self.session.execute(query.offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, group: UserGroup) -> UserGroup:
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def update(self, group: UserGroup) -> UserGroup:
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def delete(self, group: UserGroup) -> None:
        await self.session.delete(group)
        await self.session.commit()
