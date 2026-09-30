from contextlib import asynccontextmanager
from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

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

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request:Request , exc:IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail : A record with this value already exists"}
    )

app.include_router(departments_router)
app.include_router(employees_router)