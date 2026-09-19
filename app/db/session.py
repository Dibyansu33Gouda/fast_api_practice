from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession , async_sessionmaker
from app.core.config import settings
engine= create_async_engine(settings.database_url,echo=True)
SessionLocal=async_sessionmaker(engine,expire_on_commit=False)
async def get_session():
    async with SessionLocal() as session:
        yield session