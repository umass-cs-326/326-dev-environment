from typing import Optional

from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

# Type alias for header response dictionary
# This improves code readability, making it clear of
# our intent to return headers in the response
HeaderResponse = dict[str, Optional[str]]


@app.get("/items/")
def read_items(
    user_agent: Optional[str] = Header(None),
    x_token: Optional[str] = Header(None)
) -> HeaderResponse:
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return {"User-Agent": user_agent, "X-Token": x_token}
