from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company


class CompanyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(
        self, company_id: int,
    ) -> Company | None:
        result = await self.session.execute(
            select(Company).where(
                Company.id == company_id,
            ),
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, offset: int = 0, limit: int = 100,
    ) -> list[Company]:
        result = await self.session.execute(
            select(Company).offset(offset).limit(limit),
        )
        return list(result.scalars().all())

    async def create(self, company: Company) -> Company:
        try:
            self.session.add(company)
            await self.session.commit()
            await self.session.refresh(company)
            return company
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company already exists or "
                "invalid foreign key reference",
            )

    async def update(
        self, company: Company,
    ) -> Company:
        try:
            await self.session.commit()
            await self.session.refresh(company)
            return company
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update conflict or invalid "
                "foreign key reference",
            )

    async def delete(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.commit()
