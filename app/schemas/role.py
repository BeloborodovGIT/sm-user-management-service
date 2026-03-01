import datetime

from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: int
    code: str
    name: str

    model_config = {"from_attributes": True}


class RoleFunctionCreate(BaseModel):
    function_code_id: int


class RoleFunctionResponse(BaseModel):
    id: int
    role_id: int
    function_code_id: int

    model_config = {"from_attributes": True}


class UserRoleCreate(BaseModel):
    role_id: int
    active_from: datetime.date
    active_to: datetime.date | None = None


class UserRoleResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    active_from: datetime.date
    active_to: datetime.date | None

    model_config = {"from_attributes": True}
