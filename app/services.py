async def get_items_from_db(db):
    query = "SELECT * FROM items"
    items = await db.fetch_all(query)
    return items


async def create_item_in_db(db, title: str, description: str, done: bool):
    query = "INSERT INTO items(title, description, done) VALUES (:title, :description, :done) RETURNING *"
    values = {"title": title, "description": description, "done": done}
    item = await db.fetch_one(query=query, values=values)
    return item
