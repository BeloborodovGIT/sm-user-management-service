from pydantic import BaseModel


class GroupCreate(BaseModel):
    company_id: int
    group_name: str
    comment: str | None = None


class GroupUpdate(BaseModel):
    group_name: str | None = None
    comment: str | None = None


class GroupResponse(BaseModel):
    id: int
    company_id: int
    group_name: str
    comment: str | None

    model_config = {"from_attributes": True}
