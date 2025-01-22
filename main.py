from fastapi import FastAPI
from database import Base, engine
from services.shelf_service import create_shelf, get_books_on_shelf
from services.book_service import create_book
from models import BookBM, ShelfBM


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Database connected successfully!"}

@app.post("/book")
def post_shelf(book: BookBM):
    return create_book(book)

@app.post("/shelf")
def post_shelf(shelf: ShelfBM):
    return create_shelf(shelf.code)

@app.get("/shelf")
def get_shelf(shelf:ShelfBM):
    return get_books_on_shelf(shelf.code)