from fastapi import FastAPI, HTTPException
from schema import ArtifactCreate, ArtifactOut, GeoPoint

app = FastAPI(description="Artifact Management API")


def next_artifact_id():
    # Placeholder function to generate the next artifact ID
    return 1


def get_current_user_id():
    # Placeholder function to get the current user's ID
    return 1


def store_artifact_in_db(artifact: ArtifactCreate, owner_id: int) -> int:
    # Placeholder function to store the artifact in the database
    # and return the new artifact's ID
    return 1


def find_artifact_in_db(artifact_id: int) -> ArtifactOut:
    # Placeholder function to find an artifact in the database by ID
    # and return it as an ArtifactOut object
    return ArtifactOut(
        id=artifact_id,
        name="Sample Artifact",
        description="This is a sample artifact.",
        location=GeoPoint(lat=0.0, lon=0.0, alt=0.0),
        owner_id=1,
        parent_id=None,
        children=[1],
    )


# POST /api/artifact/
# This endpoint creates a new artifact. It expects a JSON body
# with the artifact details. The shape of the request body is defined
# as ArtifactCreate in schema.py. The response will be the created
# in the shape of ArtifactOut.
@app.post("/api/artifact/create", response_model=ArtifactOut)
def create_artifact(artifact: ArtifactCreate):
    try:
        current_id = next_artifact_id()
        artifact_id = store_artifact_in_db(artifact, current_id)
        out = ArtifactOut(
            id=artifact_id,
            name=artifact.name,
            description=artifact.description,
            location=artifact.location,
            owner_id=get_current_user_id(),
            parent_id=artifact.parent_id,
            children=[],
        )

        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET /api/artifact/{id}
# This endpoint retrieves artifacts. If an artifact_id query parameter
# is provided, it returns the artifact with that ID. If no ID is provided,
# it returns all artifacts. The response is a list of ArtifactOut objects.
# Note, even when a single artifact is requested, it is returned
# as a list with one item.
@app.get("/api/artifact/{artifact_id}", response_model=ArtifactOut)
def get_artifact_by_id(artifact_id: int):
    try:
        artifact = find_artifact_in_db(artifact_id)
        return artifact
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("Running Artifact Management API on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
