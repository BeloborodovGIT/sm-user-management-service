from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company


class CompanyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, company_id: int) -> Company | None:
        result = await self.session.execute(
            select(Company).where(Company.id == company_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Company]:
        result = await self.session.execute(
            select(Company).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, company: Company) -> Company:
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def update(self, company: Company) -> Company:
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def delete(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.commit()
