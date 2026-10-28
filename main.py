from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="BookStore REST API",
    description="CRUD API with Pydantic validation",
    version="1.0.0",
)


# Request model: validates incoming book data
class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    published_year: int = Field(ge=1000, le=2100)


# Response model includes the book ID
class Book(BookCreate):
    id: int


# Temporary in-memory storage
books: dict[int, Book] = {}
next_id = 1


@app.get("/")
def home():
    return {"message": "Welcome to BookStore API"}


# READ all books, with optional filters
@app.get("/books", response_model=list[Book])
def get_books(
    author: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
):
    result = list(books.values())

    if author:
        result = [
            book for book in result
            if author.lower() in book.author.lower()
        ]

    if min_price is not None:
        result = [b for b in result if b.price >= min_price]

    if max_price is not None:
        result = [b for b in result if b.price <= max_price]

    return result


# READ one book
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


# CREATE a book
@app.post("/books", response_model=Book, status_code=201)
def create_book(book_data: BookCreate):
    global next_id

    book = Book(id=next_id, **book_data.model_dump())
    books[next_id] = book
    next_id += 1

    return book


# UPDATE a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookCreate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    book = Book(id=book_id, **book_data.model_dump())
    books[book_id] = book

    return book


# DELETE a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    del books[book_id]

    return {"message": "Book deleted successfully"}