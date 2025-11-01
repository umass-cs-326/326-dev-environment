## 10. Header Parameters

In this step, we will explore how to handle header parameters in FastAPI. Header parameters are often used for passing metadata such as authentication tokens, content types, and custom headers.

### Example: Using Header Parameters

```python
from fastapi import FastAPI, Header, HTTPException
from typing import Optional

app = FastAPI()

@app.get("/items/")
def read_items(user_agent: Optional[str] = Header(None), x_token: Optional[str] = Header(None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"User-Agent": user_agent, "X-Token": x_token}
```

> NOTE: The example file `main.py` includes additional details for a complete working example. We also include `test_api.py` for testing the header functionality. Please study those files for a full implementation and understanding.

In this example, we define a FastAPI endpoint `/items/` that reads two header parameters: `User-Agent` and `X-Token`. The `X-Token` header is validated against a predefined value, and if it does not match, a 400 Bad Request error is raised.

- `User-Agent` is an optional header that can be used to identify the client making the request. It might be important to only log or process requests from certain user agents.

- `X-Token` is a custom header that we use for simple token-based authentication. In a real-world application, you would likely implement a more robust authentication mechanism such as OAuth2 or JWT.