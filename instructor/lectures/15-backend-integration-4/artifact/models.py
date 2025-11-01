# models.py

# Field from sqlmodel and Pylance have an ongoing toxic relationship.
#
# Type checking is a noble idea—like Plato’s ideal forms—but real-world
# libraries are messy, mortal, and occasionally badly typed. sqlmodel’s
# Field is one of those: so overladen with overloads that Pyright loses
# its mind. We could spend hours soothing the type checker’s insecurities,
# or we could just tape its mouth shut.
#
# In the name of sanity (and emotional well-being), we choose the latter.
# pyright: reportUnknownVariableType=none


from typing import Optional

from schema import Role
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    role: Role = Field(default=Role.creator)
    password_hash: str


class Artifact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    description: Optional[str] = None

    lat: float
    lon: float
    alt: Optional[float] = None

    owner_id: int = Field(foreign_key="user.id")
    parent_id: Optional[int] = Field(default=None,
                                     foreign_key="artifact.id")

# --- basic smoke tests -------------------------------------------------------


if __name__ == "__main__":
    import os

    from sqlmodel import Session, SQLModel, create_engine, select

    user = os.getenv("DATABASE_USER", "app")
    pasw = os.getenv("DATABASE_PASS", "app")
    host = os.getenv("DATABASE_HOST", "dev_pg")
    port = os.getenv("DATABASE_PORT", "5432")
    name = os.getenv("DATABASE_NAME", "db")
    connstr = f"postgresql+psycopg2://{user}:{pasw}@{host}:{port}/{name}"
    engine = create_engine(connstr)

    print("[setup] creating tables...")
    SQLModel.metadata.create_all(engine)

    try:
        # --- insert data ---
        print("[insert] adding users and artifacts...")
        with Session(engine) as session:
            # users
            u1 = User(username="ada@lovelace.org", email="ada@lovelace.org",
                      role=Role.creator, password_hash="x")
            u2 = User(username="alan@turing.org",   email="alan@turing.org",
                      role=Role.admin,   password_hash="y")
            session.add(u1)
            session.add(u2)
            session.commit()
            session.refresh(u1)
            session.refresh(u2)

            # artifacts
            a1 = Artifact(
                name="Root Box",
                description=None,
                lat=42.391,
                lon=-72.526,
                alt=None,
                owner_id=u1.id,   # type: ignore[arg-type]
                parent_id=None,
            )
            session.add(a1)
            session.commit()
            session.refresh(a1)

            a2 = Artifact(
                name="Inner Pouch",
                description="Nested item",
                lat=42.392,
                lon=-72.527,
                alt=95.0,
                owner_id=u1.id,    # type: ignore[arg-type]
                parent_id=a1.id,   # type: ignore[arg-type]
            )
            session.add(a2)
            session.commit()
            session.refresh(a2)

            # --- query by id ---
            print("[query] fetching a user and artifact by id...")
            u = session.get(User, u1.id)
            assert u is not None and u.username == "ada@lovelace.org"

            a = session.get(Artifact, a1.id)
            assert a is not None and a.name == "Root Box"

            # --- query children by parent_id ---
            print("[query] fetching children by parent_id...")
            stmt = select(Artifact).where(Artifact.parent_id ==
                                          a1.id)  # type: ignore[arg-type]
            children = list(session.exec(stmt))
            assert len(children) == 1 and children[0].name == "Inner Pouch"

            # --- delete child, then parent ---
            print("[delete] deleting child then parent...")
            child = session.get(Artifact, a2.id)  # type: ignore[arg-type]
            assert child is not None
            session.delete(child)
            session.commit()

            # verify child gone
            child2 = session.get(Artifact, a2.id)  # type: ignore[arg-type]
            assert child2 is None

            parent = session.get(Artifact, a1.id)  # type: ignore[arg-type]
            assert parent is not None
            session.delete(parent)
            session.commit()

            # verify parent gone
            parent2 = session.get(Artifact, a1.id)  # type: ignore[arg-type]
            assert parent2 is None

            print("[ok] basic create, read, delete flow works")

    finally:
        print("[teardown] dropping tables...")
        SQLModel.metadata.drop_all(engine)
