import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse

from app.core.config import settings
from app.core.db import db_conf

from app.routes import item_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db_conf.connect()
        yield
    except Exception as e:
        logger.error(f"Error during lifespan: {e}")
    finally:
        await db_conf.disconnect()


app = FastAPI(
    default_response_class=ORJSONResponse,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


app.include_router(item_router, prefix=settings.API_V1_STR)
