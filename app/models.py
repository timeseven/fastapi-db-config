from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    String,
    Table,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import metadata

Item = Table(
    "items",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("done", Boolean, nullable=False, server_default="false"),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
)
