from fastapi import FastAPI, HTTPException, status
from models import Author, Book
from sqlmodel import Session, SQLModel, create_engine, delete, select

# Database setup
DATABASE_URL = "postgresql+psycopg://app:app@dev_pg:5432/db"
engine = create_engine(DATABASE_URL, echo=True)

# Create tables
SQLModel.metadata.create_all(engine)

app = FastAPI()


# Author endpoints
@app.post("/authors/")
def create_author(author: Author):
    with Session(engine) as session:
        session.add(author)
        session.commit()
        session.refresh(author)
        return author


@app.get("/authors/")
def list_authors():
    with Session(engine) as session:
        authors = session.exec(select(Author)).all()
        return authors


@app.get("/authors/{author_id}")
def get_author(author_id: int):
    with Session(engine) as session:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author


@app.patch("/authors/{author_id}")
def update_author(author_id: int, author_update: Author):
    with Session(engine) as session:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        if author_update.name is not None:  # type: ignore
            author.name = author_update.name
        if author_update.email is not None:  # type: ignore
            author.email = author_update.email

        session.add(author)
        session.commit()
        session.refresh(author)
        return author


@app.delete("/authors/{author_id}")
def delete_author(author_id: int):
    with Session(engine) as session:
        author = session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        session.delete(author)
        session.commit()
        return {"message": "Author deleted successfully"}


# Book endpoints
@app.post("/books/")
def create_book(book: Book):
    with Session(engine) as session:
        # Check if author exists
        author = session.get(Author, book.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        session.add(book)
        session.commit()
        session.refresh(book)
        return book


@app.get("/books/")
def list_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book


@app.get("/books/by-author/{author_id}")
def get_books_by_author(author_id: int):
    with Session(engine) as session:
        books = session.exec(select(Book).where(
            Book.author_id == author_id)).all()
        return books


@app.patch("/books/{book_id}")
def update_book(book_id: int, book_update: Book):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if book_update.title is not None:  # type: ignore
            book.title = book_update.title
        if book_update.year is not None:  # type: ignore
            book.year = book_update.year
        if book_update.author_id is not None:  # type: ignore
            # Check if new author exists
            author = session.get(Author, book_update.author_id)
            if not author:
                raise HTTPException(status_code=404, detail="Author not found")
            book.author_id = book_update.author_id

        session.add(book)
        session.commit()
        session.refresh(book)
        return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        session.delete(book)
        session.commit()
        return {"message": "Book deleted successfully"}


@app.delete("/reset/", status_code=status.HTTP_200_OK)
def reset_database():
    with Session(engine) as session:
        # Delete children first to satisfy FK constraints
        books_result = session.exec(delete(Book))
        authors_result = session.exec(delete(Author))
        session.commit()

        # rowcount can be None/-1 depending on the driver; coerce to int >= 0
        books_deleted = int(books_result.rowcount or 0)
        authors_deleted = int(authors_result.rowcount or 0)

        return {
            "books_deleted": books_deleted,
            "authors_deleted": authors_deleted,
            "total_deleted": books_deleted + authors_deleted,
        }
