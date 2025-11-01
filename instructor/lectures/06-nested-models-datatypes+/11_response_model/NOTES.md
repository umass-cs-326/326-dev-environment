## 11. Response Model

Not only is it important to validate incoming data, but it's equally crucial to ensure that the data your API sends back to clients is structured and validated. FastAPI allows you to define response models using Pydantic, ensuring that your responses conform to expected schemas.

```python
@app.get("/preferences", response_model=UserPreferences)
def get_preferences(session_id: Optional[str] = Cookie(None)):
    if session_id == "abc123":
        return UserPreferences(theme="dark", notifications=False)
    elif session_id == "def456":
        return UserPreferences(theme="light", notifications=True)
    else:
        raise HTTPException(status_code=401, detail="Invalid session ID")
```

> NOTE: The example file `main.py` includes additional details for a complete working example. We also include `test_api.py` for testing the response model functionality. Please study those files for a full implementation and understanding.

In this example, we specify that the `response_model` for the `/preferences` endpoint is `UserPreferences`. This means that FastAPI will validate and serialize the response data to match the `UserPreferences` model before sending it to the client. If the returned data does not conform to this model, FastAPI will raise an error.
