from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import ForeignKey, String, Integer, Table, create_engine


class Base(DeclarativeBase):
    pass


class BookBase(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    shelf_id: Mapped[int] = mapped_column(ForeignKey("shelfs.id"))

    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, year={self.year})>"


class ShelfBase(Base):
    __tablename__ = "shelfs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    books: Mapped[list[BookBase]] = relationship(
        "BookBase", back_populates="shelf", lazy="subquery"
    )

    def __repr__(self) -> str:
        return f"<Shelf(id={self.id}, code={self.code})>"


BookBase.shelf = relationship("ShelfBase", back_populates="books")


DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
