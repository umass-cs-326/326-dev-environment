# main.py
from __future__ import annotations

from typing import List

from db import DatabaseService
from fastapi import FastAPI, HTTPException
from schema import ArtifactCreate, ArtifactOut, UserIn, UserOut

app = FastAPI(description="Artifact Management API")
db = DatabaseService()

current_user: UserOut | None = None


def get_current_user_id() -> int:
    if current_user == None:
        raise Exception("User not logged in")
    return current_user.id


@app.post("/api/user/register", response_model=UserOut)
def register_user(user: UserIn) -> UserOut:
    try:
        return db.register_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user/login", response_model=UserOut)
def login_user(user: UserIn) -> UserOut:
    try:
        reg_user = db.find_user(user)

        if reg_user is None:
            raise HTTPException(status_code=404,
                                detail=f"Unknown username or password")

        # Simulate login state
        global current_user
        current_user = reg_user

        return reg_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/artifact/create", response_model=ArtifactOut)
def create_artifact(artifact: ArtifactCreate):
    try:
        return db.create_new_artifact(artifact=artifact, owner_id=get_current_user_id())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/artifact/{artifact_id}", response_model=ArtifactOut)
def get_artifact_by_id(artifact_id: int):
    try:
        return db.get_artifact_by_id(artifact_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/artifact/{artifact_id}/children", response_model=List[int])
def get_artifact_children(artifact_id: int):
    try:
        return db.get_artifact_children(artifact_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reset")
def reset():
    try:
        db.reset()
        return "reset"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
