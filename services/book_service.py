from database import SessionLocal, BookBase, ShelfBase
from datetime import datetime
from models import BookBM

def create_book(book: BookBM):
    new_book = BookBase(title = book.title, author = book.author, year = book.year)
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
        