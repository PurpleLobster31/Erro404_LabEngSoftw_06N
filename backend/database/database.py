from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# A string de conexão utiliza o driver +asyncpg
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://dev_user:dev_password@localhost:5432/app_db"
)

# echo=True exibe as queries SQL no terminal (útil em dev)
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# Dependência do FastAPI para injetar a sessão nas rotas
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session