import datetime

from pydantic import BaseModel


class UserRegister(BaseModel):
    company_id: int
    group_id: int
    timezone_id: int
    username: str
    firtsname: str
    lastname: str
    patronymic: str | None = None
    password: str
    comment: str | None = None


class UserUpdate(BaseModel):
    group_id: int | None = None
    timezone_id: int | None = None
    username: str | None = None
    firtsname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    comment: str | None = None
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
