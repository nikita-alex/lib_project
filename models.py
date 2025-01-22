from pydantic import BaseModel
from typing import Union

class Book:

    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year

    def __str__(self):
        return f'"{self.__title}" by {self.__author}, {self.__year}'

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        self.__title = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value


class Shelf:

    def __init__(self, code):
        self.code = code
        self.books = []

    def add_book(self, book):
        if isinstance(book, Book):
            self.books.append(book)
        else:
            raise TypeError("Book must be of type 'Book'")


class Library:

    def __init__(self, shelfs):
        if shelfs == None:
            self.shelfs = []
        elif type(shelfs) != list:
            raise ValueError("Shelfs must be of type 'list'")
        elif all(isinstance(shelf, Shelf) for shelf in shelfs):
            self.shelfs = shelfs
        else:
            raise ValueError("All shelfs must be of type 'Shelf'")

    def add_shelf(self, shelf):
        if isinstance(shelf, Shelf):
            if self.find_shelf(shelf.code) == None:
                self.shelfs.append(shelf)
            else:
                raise ValueError("New shelf's code is not unique")
        else:
            raise ValueError("New shelf must be of type 'Shelf'")

    def find_shelf(self, code):
        for shelf in self.shelfs:
            if shelf.code == code:
                return shelf
        return None

    def add_book_to_shelf(self, book, shelf_code):
        shelf = self.find_shelf(shelf_code)
        if shelf is not None:
            shelf.add_book(book)
        else:
            raise ValueError(f"Shelf with code {shelf_code} not found")

    def __str__(self):
        result = "Library contents:\n"
        for shelf in self.shelfs:
            result += f"Shelf {shelf.code}: {[str(book) for book in shelf.books]}\n"
        return result

class BookBM(BaseModel):
    title: str
    author: str
    year: int
    shelf_id: Union[int, None]
    id: Union[int, None]

class ShelfBM(BaseModel):
    code: str