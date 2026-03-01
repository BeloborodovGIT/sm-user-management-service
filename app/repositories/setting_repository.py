from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.settings import Setting


class SettingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(
        self, setting_id: int,
    ) -> Setting | None:
        result = await self.session.execute(
            select(Setting).where(
                Setting.id == setting_id,
            ),
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, offset: int = 0, limit: int = 100,
    ) -> list[Setting]:
        result = await self.session.execute(
            select(Setting).offset(offset).limit(limit),
        )
        return list(result.scalars().all())

    async def create(
        self, setting: Setting,
    ) -> Setting:
        try:
            self.session.add(setting)
            await self.session.commit()
            await self.session.refresh(setting)
            return setting
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Setting already exists or "
                "invalid foreign key reference",
            )

    async def update(
        self, setting: Setting,
    ) -> Setting:
        try:
            await self.session.commit()
            await self.session.refresh(setting)
            return setting
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update conflict or invalid "
                "foreign key reference",
            )

    async def delete(self, setting: Setting) -> None:
        await self.session.delete(setting)
        await self.session.commit()
