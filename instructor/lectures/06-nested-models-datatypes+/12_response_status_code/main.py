from fastapi import FastAPI, HTTPException

app = FastAPI()

ItemType = dict[str, str]

items: dict[int, ItemType] = {}


@app.post("/items/", status_code=201)
def create_item(item: ItemType) -> ItemType:
    item_id = len(items) + 1
    items[item_id] = item
    return item


@app.get("/items/{item_id}", status_code=204)
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
