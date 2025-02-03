from database import SessionLocal, BookBase, ShelfBase
from datetime import datetime
from models import BookBM
from sqlalchemy.orm import joinedload
from services.shelf_service import get_shelf_code


def create_book(book):
    new_book = BookBase(title=book.title, author=book.author, year=book.year)
    set_shelf(new_book, book.shelf_id)
    return add_book_to_database(new_book)


def set_shelf(book: BookBase, shelf_id):
    book.shelf_id = shelf_id


def add_book_to_database(book: BookBase):
    session = SessionLocal()

    try:
        session.add(book)
        session.commit()
        session.refresh(book)
        return {"message": "Book created successfully!", "book_id": book.id}
    except Exception as e:
        session.rollback()
        print(f"An error occured: {e}")
    finally:
        session.close()


def get_book_info(book_id: int):
    session = SessionLocal()
    book = session.query(BookBase).filter(BookBase.id == book_id).first()
    if book:
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "shelf_code": get_shelf_code(book.shelf_id),
        }
    else:
        return []


def get_books():
    session = SessionLocal()
    books = session.query(BookBase).options(joinedload(BookBase.shelf)).all()

    if books:
        return books
    else:
        return []


def update_book_info(book_id, title, author, year, shelf_code):
    session = SessionLocal()
    try:
        book = session.query(BookBase).filter(BookBase.id == book_id).first()
        if not book:
            return False

        shelf = session.query(ShelfBase).filter(ShelfBase.code == shelf_code).first()
        if not shelf:
            return False

        book.title = title
        book.author = author
        book.year = year
        book.shelf_id = shelf.id

        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
