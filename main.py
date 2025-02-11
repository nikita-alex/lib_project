from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from services.shelf_service import (
    create_shelf,
    get_books_on_shelf,
    get_shelf_id,
    get_all_shelves,
    change_shelf_code,
)
from services.book_service import (
    create_book,
    get_book_info,
    get_books,
    update_book_info,
    delete_book_by_id,
)
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


@app.get("/shelf/{code}")
def get_shelf_by_query(request: Request, code: str):
    books = get_books_on_shelf(code)
    return templates.TemplateResponse(
        "shelf.html", {"request": request, "books": books, "code": code}
    )


@app.post("/shelf/{code}")
def update_shelf_code(request: Request, code: str, new_code: str = Form(...)):
    if change_shelf_code(code, new_code):
        return RedirectResponse(url="/shelves", status_code=303)
    else:
        raise HTTPException(status_code=500, detail="Unexpected error")


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
        create_book(book)
    return RedirectResponse(url="/all_books", status_code=303)


@app.get("/book_creation", name="books_page")
def books_page(request: Request):
    return templates.TemplateResponse("book_creation.html", {"request": request})


@app.get("/shelves", name="shelves_page")
def shelves_page(request: Request):
    shelves = get_all_shelves()
    return templates.TemplateResponse(
        "shelves.html", {"request": request, "shelves": shelves}
    )


@app.get("/library", name="library_page")
def library_page(request: Request):
    return templates.TemplateResponse("library.html", {"request": request})


@app.get("/all_books", name="all_books")
def get_all_books(request: Request):
    books = get_books()
    return templates.TemplateResponse(
        "all_books.html", {"request": request, "books": books}
    )


@app.get("/book/edit/{book_id}")
def edit_book_page(request: Request, book_id: int):
    book = get_book_info(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse(
        "edit_book.html", {"request": request, "book": book}
    )


@app.post("/book/edit/{book_id}")
def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    shelf_code: str = Form(...),
):
    updated = update_book_info(book_id, title, author, year, shelf_code)
    if not updated:
        raise HTTPException(status_code=400, detail="Failed to update book")
    return RedirectResponse(url="/all_books", status_code=303)


@app.post("/book/delete/{book_id}")
def delete_book(request: Request, book_id: int):
    delete_book_by_id(book_id)
    return RedirectResponse(url="/all_books", status_code=303)
