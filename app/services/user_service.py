import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import (
    invalidate_superuser,
    invalidate_user,
)
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.role import UserRoleCreate
from app.schemas.user import UserRegister, UserUpdate
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def get_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        return await self.repo.get_all(offset=offset, limit=limit)

    async def register(self, data: UserRegister) -> User:
        if await self.repo.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        user = User(
            company_id=data.company_id,
            group_id=data.group_id,
            timezone_id=data.timezone_id,
            username=data.username,
            firtsname=data.firtsname,
            lastname=data.lastname,
            patronymic=data.patronymic,
            created_date=datetime.date.today(),
            password=AuthService.hash_password(data.password),
            comment=data.comment,
        )
        return await self.repo.create(user)

    async def update_user(
        self, user_id: int, data: UserUpdate,
    ) -> User:
        user = await self.get_user(user_id)
        for field, value in data.model_dump(
            exclude_unset=True,
        ).items():
            setattr(user, field, value)
        result = await self.repo.update(user)
        await invalidate_user(user_id)
        return result

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.repo.delete(user)
        await invalidate_user(user_id)
        await invalidate_superuser(user_id)

    async def get_roles(self, user_id: int) -> list[UserRole]:
        await self.get_user(user_id)
        return await self.repo.get_roles(user_id)

    async def assign_role(
        self, user_id: int, data: UserRoleCreate,
    ) -> UserRole:
        await self.get_user(user_id)
        role = UserRole(
            user_id=user_id,
            role_id=data.role_id,
            active_from=data.active_from,
            active_to=data.active_to,
        )
        result = await self.repo.add_role(role)
        await invalidate_superuser(user_id)
        return result
