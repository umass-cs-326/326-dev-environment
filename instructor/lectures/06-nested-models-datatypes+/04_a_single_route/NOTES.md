## 4. Creating a New Item (POST Request)

Let us create a basic POST endpoint to create a new item. This will involve defining a route that accepts data in the request body and returns the created item.

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
def create_item(item: Item):
    return item
```

- Recall, we use Pydantic models to define the structure of the data we expect. In this case, the `Item` model has fields for `name`, `description`, `price`, and `tax`.

- The types are used to validate the incoming data. For example, `name` is a required string, `description` is an optional string, `price` is a required float, and `tax` is an optional float.

- When we send a POST request to `/items/` with a JSON body that matches the `Item` model, FastAPI will automatically validate the data and convert it into an instance of the `Item` class. If the data is valid, it will be passed to the `create_item` function, which simply returns the item.

- If it fails, FastAPI will return a `422 Unprocessable Entity` response with details about the validation errors.
