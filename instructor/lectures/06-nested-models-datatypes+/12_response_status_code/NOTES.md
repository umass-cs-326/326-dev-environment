## 12. Response Status Code

The default response status code for a successful GET request in FastAPI is `200 OK`. However, you can customize the default status code for your endpoints using the `status_code` parameter in the route decorator.

```python
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
```

In this example, we define two endpoints:

- The `create_item` endpoint returns a `201 Created` status code when a new item is successfully created.
- The `read_item` endpoint returns a `204 No Content` status code when an item is successfully retrieved, but there is no content to return (e.g., the item was deleted).

You can also raise HTTP exceptions with specific status codes using the `HTTPException` class from `fastapi` like we do in the `read_item` endpoint when the item is not found.