import uuid
from typing import Optional

from fastapi import Cookie, FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()


class UserPreferences(BaseModel):
    """Model for user preferences."""
    theme: Optional[str] = "light"
    notifications: Optional[bool] = True


class LoginResponse(BaseModel):
    """Model for login response."""
    message: str
    session_id: str


# In-memory "database" of sessions
sessions: dict[str, UserPreferences] = {}


# NOTE: we are using response_model to automatically serialize
# the response to match the UserPreferences model
@app.get("/preferences", response_model=UserPreferences)
def get_preferences(session_id: Optional[str] = Cookie(None)):
    """Get user preferences based on session ID from cookie."""
    if session_id in sessions:
        return sessions[session_id]
    else:
        raise HTTPException(status_code=401, detail="Invalid session ID")


@app.post("/login", response_model=LoginResponse)
def login(username: str, response: Response):
    """Simulate user login and set a session ID cookie."""
    # Generate a new session ID
    session_id = str(uuid.uuid4())
    # Store session in the server (fake user preferences for demo)
    sessions[session_id] = UserPreferences(theme="dark", notifications=True)
    # Set session ID cookie
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return LoginResponse(
        message="Logged in successfully",
        session_id=session_id
    )
