from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base

from app.models import departments, employee
from app.api.routes.departments import router as departments_router
from app.api.routes.employees import router as employees_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(departments_router)
app.include_router(employees_router)