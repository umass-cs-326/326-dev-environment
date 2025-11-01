import os
from typing import List

from models import Artifact as ArtifactModel
from models import User
from schema import ArtifactCreate, ArtifactOut, GeoPoint, UserIn, UserOut
from sqlmodel import Session, SQLModel, create_engine, select


class DatabaseError(Exception):
    pass


class DatabaseService:
    def __init__(self):
        user = os.getenv("DATABASE_USER", "app")
        pasw = os.getenv("DATABASE_PASS", "app")
        host = os.getenv("DATABASE_HOST", "dev_pg")
        port = os.getenv("DATABASE_PORT", "5432")
        name = os.getenv("DATABASE_NAME", "db")
        connstr = f"postgresql+psycopg2://{user}:{pasw}@{host}:{port}/{name}"
        self.engine = create_engine(connstr)

        # Initialize Tables
        self._create_db_and_tables()

    def _create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(bind=self.engine)

    def reset(self):
        SQLModel.metadata.drop_all(bind=self.engine)
        SQLModel.metadata.create_all(bind=self.engine)

    def register_user(self, user_data: UserIn) -> UserOut:
        try:
            with Session(self.engine) as session:
                user = User(username=user_data.username,
                            email=user_data.email,
                            role=user_data.role,
                            password_hash=user_data.password)
                session.add(user)
                session.commit()
                session.refresh(user)

                user_out = UserOut(id=user.id,  # type: ignore
                                   username=user.username,
                                   email=user.email,
                                   role=user.role)

                return user_out

        except Exception as e:
            raise DatabaseError(
                f"Could not create user '{user_data.username}': {str(e)}")

    def find_user(self, user_data: UserIn) -> UserOut | None:
        try:
            with Session(self.engine) as session:
                stmt = select(User).where(User.username == user_data.username,
                                          User.password_hash == user_data.password)
                result = session.exec(stmt).first()

                if result is None:
                    return None

                user_out = UserOut(id=result.id,  # type: ignore
                                   username=result.username,
                                   email=result.email,
                                   role=result.role)

                return user_out

        except Exception as e:
            raise DatabaseError(
                f"Could not create user '{user_data.username}': {str(e)}")

    def create_new_artifact(self, artifact: ArtifactCreate, owner_id: int) -> ArtifactOut:
        try:
            with Session(self.engine) as session:
                db_row = ArtifactModel(
                    name=artifact.name,
                    description=artifact.description,
                    lat=artifact.location.lat,
                    lon=artifact.location.lon,
                    alt=artifact.location.alt,
                    owner_id=owner_id,
                    parent_id=artifact.parent_id,
                )
                session.add(db_row)
                session.commit()
                session.refresh(db_row)

                return self._artifact_model_to_schema(db_row)
        except Exception as e:
            raise DatabaseError(
                f"Could not create Artifact {artifact.name} in Database: {str(e)}")

    def get_artifact_by_id(self, artifact_id: int):
        try:
            with Session(self.engine) as session:
                row = session.get(ArtifactModel, artifact_id)
                if not row:
                    raise DatabaseError(f"Artifact {artifact_id} not found")
                return self._artifact_model_to_schema(row)
        except Exception as e:
            raise DatabaseError(
                f"Could not find Artifact with ID {artifact_id}: {str(e)}")

    def get_artifact_children(self, artifact_id: int) -> List[int]:
        with Session(self.engine) as session:
            try:
                result = session.exec(
                    select(ArtifactModel.id).where(
                        ArtifactModel.parent_id == artifact_id)
                )
                # Build an explicit List[int] and filter any theoretical None values
                children_ids: List[int] = [int(i)
                                           for i in result if i is not None]
                return children_ids

            except Exception as e:
                raise DatabaseError(
                    f"Coule not fetch children for Artifact {artifact_id}: {str(e)}")

    def _artifact_model_to_schema(self, row: ArtifactModel) -> ArtifactOut:
        # At this point (loaded from DB or post-commit), id should be set.
        assert row.id is not None

        with Session(self.engine) as session:
            try:
                result = session.exec(
                    select(ArtifactModel.id).where(
                        ArtifactModel.parent_id == row.id)
                )
                # Build an explicit List[int] and filter any theoretical None values
                children_ids: List[int] = [int(i)
                                           for i in result if i is not None]

                return ArtifactOut(
                    id=row.id,
                    name=row.name,
                    description=row.description,
                    location=GeoPoint(lat=row.lat, lon=row.lon, alt=row.alt),
                    owner_id=row.owner_id,
                    parent_id=row.parent_id,
                    children=children_ids,
                )
            except Exception as e:
                raise DatabaseError(
                    f"Coule not fetch children for Artifact {row.id} {row.name}: {str(e)}")
