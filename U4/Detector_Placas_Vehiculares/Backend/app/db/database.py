from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
# configuracion de la base de datos sqlite
DATABASE_URL = "sqlite+aiosqlite:///./app/db/placas.db"

# crear el motor de la base de datos y la session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()