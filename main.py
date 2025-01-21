from database import init_db
from services.book_service import add_book_to_db


def main():
    init_db()
    print("Database initialized.")


if __name__ == "__main__":
    main()
