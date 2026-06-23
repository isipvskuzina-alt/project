from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, Session

engine = create_engine("sqlite:///library.db", echo=True)
print(engine)


Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id         = Column(Integer, primary_key=True)
    name       = Column(String, nullable=False)
    birth_year = Column(Integer)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', birth_year={self.birth_year})>"


class Book(Base):
    __tablename__ = "books"

    id        = Column(Integer, primary_key=True)
    title     = Column(String, nullable=False)
    year      = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', year={self.year})>"


Base.metadata.create_all(engine)


with Session(engine) as session:

    author1 = Author(name="Николай Гоголь",              birth_year=1809)
    author2 = Author(name="Фёдор Достоевский",           birth_year=1821)
    author3 = Author(name="Александр Солженицын",        birth_year=1918)

    book1 = Book(title="Мёртвые души",                   year=1842, author=author1)
    book2 = Book(title="Ревизор",                        year=1836, author=author1)
    book3 = Book(title="Преступление и наказание",       year=1866, author=author2)
    book4 = Book(title="Идиот",                          year=1869, author=author2)
    book5 = Book(title="Архипелаг ГУЛАГ",                year=1973, author=author3)

    session.add_all([author1, author2, author3, book1, book2, book3, book4, book5])
    session.commit()
    print("Авторы и книги добавлены.")

    print("\nВсе авторы:")
    authors = session.query(Author).all()
    for a in authors:
        print(f"  {a.name} ({a.birth_year})")

    gogol = session.query(Author).filter_by(name="Николай Гоголь").first()
    gogol.name = "Николай Васильевич Гоголь"
    session.commit()
    print(f"\nИмя изменено: {gogol.name}")

    book_to_delete = session.query(Book).filter_by(title="Ревизор").first()
    session.delete(book_to_delete)
    session.commit()
    print("Книга удалена: Ревизор")

    print("\nВсе книги (от новых к старым):")
    books_sorted = session.query(Book).order_by(Book.year.desc()).all()
    for b in books_sorted:
        print(f"  {b.title} ({b.year})")

    print("\nКниги, изданные после 1950 года:")
    books_after_1950 = session.query(Book).filter(Book.year > 1950).all()
    for b in books_after_1950:
        print(f"  {b.title} ({b.year})")

    target_name = "Александр Солженицын"
    found_author = session.query(Author).filter(Author.name == target_name).first()
    print(f"\nПоиск автора '{target_name}': {found_author}")

    book_count = session.query(func.count(Book.id)).scalar()
    print(f"\nОбщее количество книг в БД: {book_count}")

    print("\nПервые 3 книги по алфавиту:")
    first_three = session.query(Book).order_by(Book.title).limit(3).all()
    for b in first_three:
        print(f"  {b.title}")

print("\nВсе операции выполнены успешно.")