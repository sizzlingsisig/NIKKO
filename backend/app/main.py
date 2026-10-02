"""FastAPI app assembly: lifespan bootstrap, CORS, router wiring.

Startup does two idempotent things: create the SQLite schema (PRD §5)
and make sure the object bucket exists (FR-5). Neither step may take the
API down — a stopped storage node degrades uploads, it shouldn't kill
health checks.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config, db, storage
from .routers import admin, health, register

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    try:
        storage.ensure_bucket(storage.get_client(), config.S3_BUCKET)
    except Exception as exc:  # noqa: BLE001 - storage may not be up yet
        logger.warning("Bucket check skipped (%s): %s", config.S3_BUCKET, exc)
    yield


app = FastAPI(title="Form5 Portal API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(register.router)
app.include_router(admin.router)
