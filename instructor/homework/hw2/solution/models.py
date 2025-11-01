from typing import Optional

from sqlmodel import Field, SQLModel  # type: ignore


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int = Field(ge=1000, le=2100)
    author_id: int = Field(foreign_key="author.id")
    author_id: int = Field(foreign_key="author.id")
