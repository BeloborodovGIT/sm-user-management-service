import datetime

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    company_id: int = Field(gt=0)
    group_id: int = Field(gt=0)
    timezone_id: int = Field(gt=0)
    username: str = Field(min_length=1, max_length=60)
    firtsname: str = Field(min_length=1, max_length=60)
    lastname: str = Field(min_length=1, max_length=60)
    patronymic: str | None = Field(
        default=None, max_length=60,
    )
    password: str = Field(min_length=8, max_length=255)
    comment: str | None = Field(
        default=None, max_length=1000,
    )


class UserUpdate(BaseModel):
    group_id: int | None = Field(default=None, gt=0)
    timezone_id: int | None = Field(
        default=None, gt=0,
    )
    username: str | None = Field(
        default=None, min_length=1, max_length=60,
    )
    firtsname: str | None = Field(
        default=None, min_length=1, max_length=60,
    )
    lastname: str | None = Field(
        default=None, min_length=1, max_length=60,
    )
    patronymic: str | None = Field(
        default=None, max_length=60,
    )
    comment: str | None = Field(
        default=None, max_length=1000,
    )
    user_lock: bool | None = None


class UserResponse(BaseModel):
    id: int
    company_id: int
    group_id: int
    timezone_id: int
    username: str
    firtsname: str
    lastname: str
    patronymic: str | None
    created_date: datetime.date
    user_lock: bool
    comment: str | None

    model_config = {"from_attributes": True}
