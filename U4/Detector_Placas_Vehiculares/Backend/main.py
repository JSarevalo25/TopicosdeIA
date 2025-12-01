from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI

from app.api.routes import router as placas_router
from app.api.correo_routes import router as correo_router
from app.db.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = Path(__file__).resolve().parent / "db" / "placas.db"
    if not db_path.exists():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(placas_router, prefix="/placas", tags=["placas"])

app.include_router(correo_router, prefix="/correo", tags=["correo"])

