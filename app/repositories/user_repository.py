from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id),
        )
        return result.scalar_one_or_none()

    async def get_by_username(
        self, username: str,
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username),
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, offset: int = 0, limit: int = 100,
    ) -> list[User]:
        result = await self.session.execute(
            select(User).offset(offset).limit(limit),
        )
        return list(result.scalars().all())

    async def create(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists or invalid "
                "foreign key reference",
            )

    async def update(self, user: User) -> User:
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update conflict or invalid "
                "foreign key reference",
            )

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def get_roles(
        self, user_id: int,
    ) -> list[UserRole]:
        result = await self.session.execute(
            select(UserRole).where(
                UserRole.user_id == user_id,
            ),
        )
        return list(result.scalars().all())

    async def add_role(self, role: UserRole) -> UserRole:
        try:
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(role)
            return role
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role assignment conflict or "
                "invalid role reference",
            )
