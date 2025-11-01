## 9. Cookie Example

```python
from fastapi import FastAPI, Cookie, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserPreferences(BaseModel):
    theme: Optional[str] = "light"
    notifications: Optional[bool] = True

@app.get("/preferences", response_model=UserPreferences)
def get_preferences(session_id: Optional[str] = Cookie(None)):
    if session_id == "abc123":
        return UserPreferences(theme="dark", notifications=False)
    elif session_id == "def456":
        return UserPreferences(theme="light", notifications=True)
    else:
        raise HTTPException(status_code=401, detail="Invalid session ID")
```

> NOTE: The example file `main.py` includes additional details for a complete working example. We also include `test_api.py` for testing the cookie functionality. Please study those files for a full implementation and understanding.

In this example, we define a FastAPI endpoint `/preferences` that reads a cookie named `session_id`. Depending on the value of this cookie, it returns different user preferences. If the cookie is missing or has an invalid value, it raises a 401 Unauthorized error.

### Cookie Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client, Server: Step 1: User Login
    Client->>Server: POST /login?username=testuser
    Server->>Server: Generate session_id (UUID)
    Server->>Server: Store session in memory
    Server->>Client: 200 OK + Set-Cookie with session_id and HttpOnly flag
    
    Note over Client, Server: Step 2: Client stores cookie automatically
    Client->>Client: Browser saves cookie
    
    Note over Client, Server: Step 3: Access Protected Resource
    Client->>Server: GET /preferences (Cookie: session_id=abc123)
    Server->>Server: Validate session_id
    Server->>Server: Retrieve user preferences
    Server->>Client: 200 OK (theme: dark, notifications: true)
    
    Note over Client, Server: Step 4: Invalid/Missing Cookie Example
    Client->>Server: GET /preferences (no cookie or invalid session)
    Server->>Server: Session validation fails
    Server->>Client: 401 Unauthorized (Invalid session ID)
```

When a client makes a request to this endpoint with the appropriate cookie, they will receive a JSON response with their preferences. For example:

```http
GET /preferences HTTP/1.1
Host: example.com
Cookie: session_id=abc123
```

Response:

```json
{
    "theme": "dark",
    "notifications": false
}
```
