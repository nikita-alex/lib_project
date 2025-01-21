from database import SessionLocal, BookBase, ShelfBase


def create_shelf(code):
    session = SessionLocal()
    try:
        new_shelf = ShelfBase(code=code)
        session.add(new_shelf)
        session.commit
        print("Shelf added successfully!")
    except Exception as e:
        session.rollback
        print(f"An error occurred: {e}")
    finally:
        session.close
