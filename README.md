# FastAPI Database Configuration 

## Overview

This project implements an asynchronous database configuration using FastAPI, Databases, PostgreSQL, SQLAlchemy, and Alembic. SQLAlchemy and Alembic are utilized for defining the database model and handling database migrations. The Databases library is employed for creating a connection pool and interacting with the database using raw SQL.


## Features

- 🔌 Asynchronous database connection pooling
- 🔒 Configurable transaction isolation levels
- 🛡️ Dependency injection for database connections
- 📊 Flexible connection pool management

## Prerequisites

- Python 3.13.2
- FastAPI
- Databases
- SQLAlchemy
- Alembic
- Database driver (e.g., asyncpg for PostgreSQL)

## Configuration Parameters

The database configuration supports the following parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `url` | Database connection string | Required |
| `min_size` | Minimum connection pool size | 10 |
| `max_size` | Maximum connection pool size | 20 |
| `timeout` | Connection timeout (seconds) | 30.0 |
| `max_inactive_connection_lifetime` | Max inactive connection time (seconds) | 180.0 |

## Transaction Types

The configuration provides three database dependency types:

1. **Write Transaction** (`write_db_transaction`)
   - Isolation Level: Read Committed
   - Read/Write Access
   - Suitable for write operations

2. **Read Transaction** (`read_db_transaction`)
   - Isolation Level: Repeatable Read
   - Read-Only Access
   - Ideal for complex read queries

3. **Simple Read/Write** (`get_db`)
   - Direct pool access
   - Suitable for single, simple queries

## Usage Example

```python
from fastapi import APIRouter

from app.schemas import ItemIn, ItemOut
from app.core.deps import SimpleDbDep, WriteDbDep

item_router = APIRouter(
    prefix="/items",
    tags=["Items"],
)

async def get_items_from_db(db):
    query = "SELECT * FROM items"
    items = await db.fetch_all(query)
    return items


async def create_item_in_db(db, title: str, description: str, done: bool):
    query = "INSERT INTO items(title, description, done) VALUES (:title, :description, :done) RETURNING *"
    values = {"title": title, "description": description, "done": done}
    item = await db.fetch_one(query=query, values=values)
    return item


@item_router.get("/", response_model=list[ItemOut])
async def get_items(db: SimpleDbDep):
    items = await get_items_from_db(db)
    return [ItemOut(**item).model_dump() for item in items]


@item_router.post("/", response_model=ItemOut)
async def create_item(db: WriteDbDep, item: ItemIn):
    item = await create_item_in_db(db, item.title, item.description, item.done)
    return ItemOut(**item).model_dump()

```

## Connection Lifecycle

The application uses FastAPI's `lifespan` context manager to manage the database connection throughout the application's lifecycle:
- Automatically establishes a connection to the database when the application starts
- Logs any errors encountered during the connection process.
- Ensures a clean disconnection from the database when the application shuts down.

## Environment Configuration

Recommended environment variables:
- `ENVIRONMENT`: Environment variable, e.g. local
- `PROJECT_NAME`: your-app-name, e.g. My App
- `DATABASE_URL`: your-database-url, e.g. postgresql://postgres:postgres@localhost:5432/postgres
- `ASYNC_DATABASE_URL`:your-async-database-url, e.g. postgresql+asyncpg://postgres:postgres@localhost:5432/postgres


## Get Started

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and [just](https://just.systems/man/en/packages.html) 
<br>

2. Clone the project and install denpedencies

```bash
git clone https://github.com/timeseven/fastapi-db-config.git
cd fastapi-db-config
uv sync
```
<br>

3. Create the database locally using docker compose(docker-compose.yml)
```bash
version: "3.8"

services:
  db:
    image: postgres:14-alpine
    container_name: postgres
    ports:
      - 5432:5432
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
    driver: local
```
<br>

4. Set the environment variables in .env.dev and change it to .env
<br>

5. Migrate the database using just
```bash
just migrate
```
<br>

6. Run the project using just
```bash
just run
```


### Lisence

[MIT](./LICENSE)



