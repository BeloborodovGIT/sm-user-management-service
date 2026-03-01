from datetime import date

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_access_token
from app.database import get_db
from app.models.dictionaries import RolesDict
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SUPERUSER_ROLE_CODE = "superuser"

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient privileges",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception
    user: User | None = await UserRepository(session).get_by_id(user_id)
    if user is None or user.user_lock:
        raise credentials_exception
    return user


async def _user_has_superuser_role(
    user_id: int, session: AsyncSession,
) -> bool:
    today = date.today()
    result = await session.execute(
        select(UserRole.id)
        .join(RolesDict, UserRole.role_id == RolesDict.id)
        .where(
            UserRole.user_id == user_id,
            RolesDict.code == SUPERUSER_ROLE_CODE,
            UserRole.active_from <= today,
            (UserRole.active_to >= today) | (UserRole.active_to.is_(None)),
        )
        .limit(1)
    )
    return result.first() is not None


async def get_superuser(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    user = await get_current_user(token=token, session=session)
    if not await _user_has_superuser_role(user.id, session):
        raise forbidden_exception
    return user


async def get_self_or_superuser(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    current_user = await get_current_user(token=token, session=session)
    if current_user.id == user_id:
        return current_user
    if not await _user_has_superuser_role(current_user.id, session):
        raise forbidden_exception
    return current_user


async def get_own_company_or_superuser(
    company_id: int,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    current_user = await get_current_user(token=token, session=session)
    if current_user.company_id == company_id:
        return current_user
    if not await _user_has_superuser_role(current_user.id, session):
        raise forbidden_exception
    return current_user
