from database import SessionLocal, ShelfBase
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
        return [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "year": book.year,
            }
            for book in shelf.books
        ]
    else:
        return []


def get_shelf_id(shelf_code):
    session = SessionLocal()
    shelf = session.query(ShelfBase).filter(ShelfBase.code == shelf_code).first()
    if shelf:
        return shelf.id
    else:
        return None


def get_shelf_code(shelf_id):
    session = SessionLocal()
    shelf = session.query(ShelfBase).filter(ShelfBase.id == shelf_id).first()
    if shelf:
        return shelf.code
    else:
        return None


def get_all_shelves():
    session = SessionLocal()
    shelves = session.query(ShelfBase).all()
    if shelves:
        return shelves
    else:
        return None


def change_shelf_code(code, new_code):
    session = SessionLocal()
    try:
        shelf = session.query(ShelfBase).filter(ShelfBase.code == code).first()
        if shelf:
            shelf.code = new_code
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(e)
        return False
    finally:
        session.close()


def delete_shelf(code):
    if get_books_on_shelf(code) == []:
        session = SessionLocal()
        try:
            shelf = session.query(ShelfBase).filter(ShelfBase.code == code).first()
            session.delete(shelf)
            session.commit()
            return {"message": "Shelf deleted successfully"}
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=500, detail="Error: " + e)
        finally:
            session.close()
    else:
        raise HTTPException(status_code=422, detail="Shelf is not empty")
