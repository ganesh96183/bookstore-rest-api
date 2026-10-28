BookStore REST API

A REST API built using Python, FastAPI, and Pydantic for managing books.

Features

- Create a book
- Retrieve all books
- Retrieve a book by ID
- Update book details
- Delete a book
- Validate book data using Pydantic
- Interactive API documentation using Swagger UI

Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn

Run Locally

Install dependencies:

python -m pip install fastapi uvicorn pydantic

Start the server:

python -m uvicorn main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

Validation

The API rejects invalid book data, such as a price less than or equal to zero.

Author

Ganesh
