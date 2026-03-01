from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await UserRepository(self.session).get_by_username(username)
        if user is None or not pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )
        if user.user_lock:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is locked",
            )
        token = create_access_token(user.id)
        return TokenResponse(access_token=token)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
