# Artifact Schemas
from __future__ import annotations  # for forward references in type hints

from typing import Optional, List, Annotated
from enum import StrEnum
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)

#
# Reusable Constrained Types
#


# Role enum for the user roles.
class Role(StrEnum):
    admin = "admin"
    creator = "creator"


#
# Shared value objects
#


# A GeoPoint model to represent geographical coordinates.
class GeoPoint(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    alt: Optional[float] = None


# An artifact summary for embedding in UserOut.
class ArtifactSummary(BaseModel):  # avoid cycles on UserOut
    id: int
    name: str = Field(min_length=1, max_length=100)
    location: GeoPoint


#
# User Schemas
#
class UserIn(BaseModel):  # for create or update
    username: EmailStr
    password: str = Field(min_length=12, max_length=128, pattern=r"^[!-~]+$")
    email: EmailStr
    role: Role


class UserOut(BaseModel):  # for responses
    id: int
    username: EmailStr
    email: EmailStr
    role: Role
    owns: list[ArtifactSummary] = Field(default_factory=list)


#
# Artifact Schemas
#


class ArtifactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(..., min_length=0, max_length=500)
    location: GeoPoint
    parent_id: Optional[int] = None


class ArtifactIn(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(..., min_length=0, max_length=500)
    location: GeoPoint
    owner_id: int
    parent_id: Optional[int] = None


class ArtifactOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(..., min_length=0, max_length=500)
    location: GeoPoint
    owner_id: int
    parent_id: Optional[int] = None
    children: List[ArtifactSummary] = Field(default_factory=list)


if __name__ == "__main__":
    try:
        # Not much way of testing, but at least we can instantiate them.
        point = GeoPoint(lat=37.7749, lon=-122.4194, alt=30)
        print(point)

        artifact_summary = ArtifactSummary(id=2, name="A", location=point)
        print(artifact_summary)

        user_out = UserOut(
            id=1,
            username="a@foo.com",
            email="a@foo.com",
            role=Role.creator,
            owns=[artifact_summary],
        )
        print(user_out)

        user_in = UserIn(
            username="a@foo.com",
            password="thisisapassword",
            email="a@foo.com",
            role=Role.creator,
        )
        print(user_in)

        artifact_in = ArtifactIn(
            id=1,
            name="A",
            description=None,
            location=point,
            owner_id=1,
            parent_id=None,
        )
        print(artifact_in)

        artifact_out = ArtifactOut(
            id=1,
            name="A",
            description=None,
            location=point,
            owner=user_out,
            parent_id=None,
            children=[],
        )
        print(artifact_out)

    except Exception as e:
        print(f"Error during model instantiation: {e}")
