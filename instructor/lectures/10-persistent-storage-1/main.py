from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Define models


class DiningHallBase(SQLModel):
    name: str
    location: str
    capacity: Optional[int] = None


class DiningHall(DiningHallBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class DiningHallCreate(DiningHallBase):
    pass


class DiningHallRead(DiningHallBase):
    id: int


# Create engine (Docker container named "db")
DATABASE_URL = "postgresql+psycopg://postgres:postgres@db:5432/umass_dining"
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)

# Initialize FastAPI
app = FastAPI()

# Dependency


def get_session():
    with Session(engine) as session:
        yield session

# Endpoints


@app.post("/dining-halls/", response_model=DiningHallRead)
def create_dining_hall(hall: DiningHallCreate, session: Session = Depends(get_session)):
    db_hall = DiningHall.from_orm(hall)
    session.add(db_hall)
    session.commit()
    session.refresh(db_hall)
    return db_hall


@app.get("/dining-halls/", response_model=List[DiningHallRead])
def read_dining_halls(session: Session = Depends(get_session)):
    halls = session.exec(select(DiningHall)).all()
    return halls


@app.delete("/dining-halls/{hall_id}")
def delete_dining_hall(hall_id: int, session: Session = Depends(get_session)):
    hall = session.get(DiningHall, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Dining hall not found")
    session.delete(hall)
    session.commit()
    return {"ok": True}
    return {"ok": True}
