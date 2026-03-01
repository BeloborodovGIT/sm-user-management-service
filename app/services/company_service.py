import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = CompanyRepository(session)

    async def get_company(self, company_id: int) -> Company:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
            )
        return company

    async def get_companies(self, offset: int = 0, limit: int = 100) -> list[Company]:
        return await self.repo.get_all(offset=offset, limit=limit)

    async def create_company(self, data: CompanyCreate) -> Company:
        company = Company(
            property_id=data.property_id,
            name=data.name,
            created_date=datetime.date.today(),
            inn=data.inn,
            kpp=data.kpp,
            ogrn=data.ogrn,
            bic=data.bic,
        )
        return await self.repo.create(company)

    async def update_company(self, company_id: int, data: CompanyUpdate) -> Company:
        company = await self.get_company(company_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(company, field, value)
        return await self.repo.update(company)

    async def delete_company(self, company_id: int) -> None:
        company = await self.get_company(company_id)
        await self.repo.delete(company)
