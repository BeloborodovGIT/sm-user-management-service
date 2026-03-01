import datetime

from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    property_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=255)
    inn: str = Field(min_length=10, max_length=16)
    kpp: str = Field(min_length=9, max_length=9)
    ogrn: str | None = Field(
        default=None, max_length=13,
    )
    bic: str | None = Field(
        default=None, max_length=9,
    )


class CompanyUpdate(BaseModel):
    name: str | None = Field(
        default=None, min_length=1, max_length=255,
    )
    inn: str | None = Field(
        default=None, min_length=10, max_length=16,
    )
    kpp: str | None = Field(
        default=None, min_length=9, max_length=9,
    )
    ogrn: str | None = Field(
        default=None, max_length=13,
    )
    bic: str | None = Field(
        default=None, max_length=9,
    )


class CompanyResponse(BaseModel):
    id: int
    property_id: int
    name: str
    created_date: datetime.date
    inn: str
    kpp: str
    ogrn: str | None
    bic: str | None

    model_config = {"from_attributes": True}
