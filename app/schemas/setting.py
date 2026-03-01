import datetime

from pydantic import BaseModel


class SettingCreate(BaseModel):
    setting_code_id: int
    value: str
    active_from: datetime.date
    active_to: datetime.date | None = None


class SettingUpdate(BaseModel):
    value: str | None = None
    active_to: datetime.date | None = None


class SettingResponse(BaseModel):
    id: int
    setting_code_id: int
    value: str
    active_from: datetime.date
    active_to: datetime.date | None

    model_config = {"from_attributes": True}
