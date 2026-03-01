import datetime

from pydantic import BaseModel, Field


class SettingCreate(BaseModel):
    setting_code_id: int = Field(gt=0)
    value: str = Field(min_length=1, max_length=255)
    active_from: datetime.date
    active_to: datetime.date | None = None


class SettingUpdate(BaseModel):
    value: str | None = Field(
        default=None, min_length=1, max_length=255,
    )
    active_to: datetime.date | None = None


class SettingResponse(BaseModel):
    id: int
    setting_code_id: int
    value: str
    active_from: datetime.date
    active_to: datetime.date | None

    model_config = {"from_attributes": True}
