from database import SessionLocal, BookBase, ShelfBase
from datetime import datetime


def create_book(title, author, year):
    new_book = BookBase(title=title, author=author, year=year)
    return new_book


def set_shelf(book, shelf):
    book.shelf_id = shelf


def add_book_to_database(book: BookBase):
    session = SessionLocal()

    try:
        session.add(book)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occured: {e}")
    finally:
        session.close()
