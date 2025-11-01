# Artifact Schemas
from __future__ import annotations

from enum import StrEnum
from typing import Annotated, List, Optional

from pydantic import BaseModel, EmailStr, Field, StringConstraints

# Role enum for the user roles.


class Role(StrEnum):
    admin = "admin"
    creator = "creator"

# Shared value objects


class GeoPoint(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    alt: Optional[float] = None


# User Schemas
Password = Annotated[str, StringConstraints(
    min_length=12, max_length=128, pattern=r"^[!-~]+$")]


class UserIn(BaseModel):  # for create or update
    username: EmailStr
    password: Password
    email: EmailStr
    role: Role


class UserOut(BaseModel):  # for responses
    id: int
    username: EmailStr
    email: EmailStr
    role: Role
    # owns: list[ArtifactSummary] = Field(default_factory=list)
    owns: List[int] = Field(default_factory=list)  # type: ignore

# Artifact Schemas


class ArtifactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        default=None, min_length=0, max_length=500)
    location: GeoPoint
    parent_id: Optional[int] = None


class ArtifactIn(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        default=None, min_length=0, max_length=500)
    location: GeoPoint
    owner_id: int
    parent_id: Optional[int] = None


class ArtifactOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(
        default=None, min_length=0, max_length=500)
    location: GeoPoint
    owner_id: int
    parent_id: Optional[int] = None
    # children: List[ArtifactSummary] = Field(default_factory=list)
    children: List[int] = Field(default_factory=list)  # type: ignore


if __name__ == "__main__":
    try:
        # Sanity checks
        point = GeoPoint(lat=37.7749, lon=-122.4194, alt=30)

        user_out = UserOut(
            id=1,
            username="a@foo.com",
            email="a@foo.com",
            role=Role.creator,
            owns=[2],
        )

        user_in = UserIn(
            username="a@foo.com",
            password="thisisapassword",
            email="a@foo.com",
            role=Role.creator,
        )

        artifact_in = ArtifactIn(
            id=1,
            name="A",
            description=None,
            location=point,
            owner_id=1,
            parent_id=None,
        )

        artifact_out = ArtifactOut(
            id=1,
            name="A",
            description=None,
            location=point,
            owner_id=user_out.id,  # was "owner=user_out"
            parent_id=None,
            children=[2],
        )

        print(point)
        print(user_out)
        print(user_in)
        print(artifact_in)
        print(artifact_out)

    except Exception as e:
        print(f"Error during model instantiation: {e}")
