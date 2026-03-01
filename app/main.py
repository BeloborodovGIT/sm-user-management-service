from contextlib import asynccontextmanager

import app.models  # noqa: F401
from fastapi import FastAPI

from app.database import engine
from app.routers import (
    auth, companies, groups, roles,
    settings as settings_router, users,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="User Management Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    auth.router, prefix="/api/v1",
)
app.include_router(
    users.router, prefix="/api/v1",
)
app.include_router(
    companies.router, prefix="/api/v1",
)
app.include_router(
    groups.router, prefix="/api/v1",
)
app.include_router(
    roles.router, prefix="/api/v1",
)
app.include_router(
    settings_router.router, prefix="/api/v1",
)
