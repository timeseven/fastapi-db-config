from databases import Database
from fastapi import Depends
from typing import Annotated, AsyncGenerator

from app.core.db import db_conf


# Acquire a transaction for write operations as db dependency
async def write_db_transaction() -> AsyncGenerator[Database, None]:
    async with db_conf.db_pool.transaction(
        isolation="read_committed", readonly=False, deferrable=False
    ):
        yield db_conf.db_pool


# Acquire a read-only transaction for multiple queries as db dependency
async def read_db_transaction() -> AsyncGenerator[Database, None]:
    async with db_conf.db_pool.transaction(
        isolation="repeatable_read", readonly=True, deferrable=True
    ):
        yield db_conf.db_pool


# Directly yield the databases pool for single query as db dependency
async def get_db() -> AsyncGenerator[Database, None]:
    yield db_conf.db_pool


WriteDbDep = Annotated[Database, Depends(write_db_transaction)]
ReadDbDep = Annotated[Database, Depends(read_db_transaction)]
SimpleDbDep = Annotated[Database, Depends(get_db)]
