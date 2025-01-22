from fastapi import FastAPI
from database import Base, engine
from pydantic import BaseModel
from typing import Union
from services.shelf_service import create_shelf, get_books_on_shelf

class Book(BaseModel):
    title: str
    author: str
    year: int
    shelf: Union[str, None]

class Shelf(BaseModel):
    code: str

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Database connected successfully!"}

@app.post("/shelf")
def post_shelf(shelf: Shelf):
    return create_shelf(shelf.code)

@app.get("/shelf")
def get_shelf(shelf:Shelf):
    return {"books": get_books_on_shelf(shelf.code)}