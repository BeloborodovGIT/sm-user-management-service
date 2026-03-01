from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    company_id: int = Field(gt=0)
    group_name: str = Field(
        min_length=1, max_length=255,
    )
    comment: str | None = Field(
        default=None, max_length=1000,
    )


class GroupUpdate(BaseModel):
    group_name: str | None = Field(
        default=None, min_length=1, max_length=255,
    )
    comment: str | None = Field(
        default=None, max_length=1000,
    )


class GroupResponse(BaseModel):
    id: int
    company_id: int
    group_name: str
    comment: str | None

    model_config = {"from_attributes": True}
