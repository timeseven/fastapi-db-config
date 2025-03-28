from fastapi import APIRouter

from app.core.deps import SimpleDbDep, WriteDbDep
from app.schemas import ItemIn, ItemOut
from app.services import get_items_from_db, create_item_in_db

item_router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@item_router.get("/", response_model=list[ItemOut])
async def get_items(db: SimpleDbDep):
    items = await get_items_from_db(db)
    return [ItemOut(**item).model_dump() for item in items]


@item_router.post("/", response_model=ItemOut)
async def create_item(db: WriteDbDep, item: ItemIn):
    item = await create_item_in_db(db, item.title, item.description, item.done)
    return ItemOut(**item).model_dump()
