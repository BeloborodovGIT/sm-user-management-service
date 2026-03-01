import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    property_id: int
    name: str
    inn: str
    kpp: str
    ogrn: str | None = None
    bic: str | None = None


class CompanyUpdate(BaseModel):
    name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    ogrn: str | None = None
    bic: str | None = None


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
