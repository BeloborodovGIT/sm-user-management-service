from contextlib import asynccontextmanager

import app.models  # noqa: F401 — ensure all models are registered
from fastapi import FastAPI

from app.database import engine, Base
from app.routers import auth, companies, groups, roles, settings, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="User Management Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(companies.router, prefix="/api/v1")
app.include_router(groups.router, prefix="/api/v1")
app.include_router(roles.router, prefix="/api/v1")
app.include_router(settings.router, prefix="/api/v1")
