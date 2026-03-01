from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.settings import Setting
from app.repositories.setting_repository import SettingRepository
from app.schemas.setting import SettingCreate, SettingUpdate


class SettingService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = SettingRepository(session)

    async def get_setting(self, setting_id: int) -> Setting:
        setting = await self.repo.get_by_id(setting_id)
        if not setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found"
            )
        return setting

    async def get_settings(self, offset: int = 0, limit: int = 100) -> list[Setting]:
        return await self.repo.get_all(offset=offset, limit=limit)

    async def create_setting(self, data: SettingCreate) -> Setting:
        setting = Setting(
            setting_code_id=data.setting_code_id,
            value=data.value,
            active_from=data.active_from,
            active_to=data.active_to,
        )
        return await self.repo.create(setting)

    async def update_setting(self, setting_id: int, data: SettingUpdate) -> Setting:
        setting = await self.get_setting(setting_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(setting, field, value)
        return await self.repo.update(setting)

    async def delete_setting(self, setting_id: int) -> None:
        setting = await self.get_setting(setting_id)
        await self.repo.delete(setting)
