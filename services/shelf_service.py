from database import SessionLocal, BookBase, ShelfBase
from fastapi import HTTPException

def create_shelf(code):
    session = SessionLocal()
    try:
        new_shelf = ShelfBase(code=code)
        session.add(new_shelf)
        session.commit()
        session.refresh(new_shelf)
        return {"message": "Shelf created successfully!", "shelf_id": new_shelf.id} 
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating shelf: {e}")
    finally:
        session.close


def get_books_on_shelf(shelf_code):
    session = SessionLocal()
    shelf = session.query(ShelfBase).filter(ShelfBase.code == shelf_code).first()
    if shelf:
        return [book.title for book in shelf.books]
    else:
        return [] 
