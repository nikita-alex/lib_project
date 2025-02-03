from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from services.shelf_service import create_shelf, get_books_on_shelf, get_shelf_id
from services.book_service import create_book, get_book_info
from models import BookBM, ShelfBM


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/shelf")
def get_shelf_by_query(request: Request, code: str):
    books = get_books_on_shelf(code)
    return templates.TemplateResponse(
        "shelf.html", {"request": request, "books": books, "code": code}
    )


@app.post("/shelf")
def post_shelf(code: str = Form(...)):
    create_shelf(code)
    return {"message": "Shelf created!"}


@app.get("/book")
def get_book(id: int):
    return get_book_info(id)


@app.post("/book")
def post_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    shelf_code: str = Form(...),
):

    shelf_id = get_shelf_id(shelf_code)
    if shelf_id == None:
        raise HTTPException(status_code=404, detail="Shelf not found")
    else:
        book = BookBM(title=title, author=author, year=year, shelf_id=shelf_id, id=None)
    return create_book(book)


@app.get("/book_creation", name="books_page")
def books_page(request: Request):
    return templates.TemplateResponse("book_creation.html", {"request": request})


@app.get("/shelves", name="shelves_page")
def shelves_page(request: Request):
    return templates.TemplateResponse("shelves.html", {"request": request})


@app.get("/library", name="library_page")
def library_page(request: Request):
    return templates.TemplateResponse("library.html", {"request": request})
