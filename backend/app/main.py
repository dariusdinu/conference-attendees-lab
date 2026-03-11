from fastapi import FastAPI
from pathlib import Path
from sqlalchemy import select, func

from .db import create_tables, db_ping, get_engine, get_session_factory
from .models import Attendee
from .seed import seed_from_csv
from .routes import router as users_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app):
    create_tables(_engine)

    with _SessionLocal() as session:
        count = session.execute(select(func.count()).select_from(Attendee)).scalar_one()
        if count == 0:
            seed_from_csv(session, Path("/app/seed_attendees.csv"))

    yield

app = FastAPI(title="Conference Attendees API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_engine = get_engine()
_SessionLocal = get_session_factory(_engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    db_ping(_engine)
    return {"status": "ok", "db": "reachable"}

app.include_router(users_router)