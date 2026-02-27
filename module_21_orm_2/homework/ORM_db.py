from datetime import date, datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Date, Table, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, mapper, declarative_base, relationship, backref

engine = create_engine("sqlite:///./library.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


book_student_association = Table(
    'book_student_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True)
)

class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    books = relationship("Books",
                         backref=backref("author", lazy='select'),
                         cascade="all, delete-orphan")

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    receiving_books = relationship("ReceivingBooks",
                                  backref=backref("book", lazy='joined'),
                                  cascade="all, delete-orphan")

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    books = association_proxy('receiving_books', 'book')

    receiving_books = relationship("ReceivingBooks",
                                   backref=backref("student", lazy='select'),
                                   cascade="all, delete-orphan")

    @classmethod
    def get_scholarship_students(cls, session):
        return session.query(cls).filter_by(scholarship=True).all()

    @classmethod
    def get_high_score_students(cls, session, score):
        return session.query(cls).filter(cls.average_score > score).all()


class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, nullable=True)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return.date() - self.date_of_issue.date()).days
        else:
            return (date.today() - self.date_of_issue.date()).days


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()

    # Создание связанных данных
    author = Authors(name="Лев", surname="Толстой")
    book = Books(name="Война и мир", count=3, release_date=date(1865, 1, 1), author=author)
    student = Students(name="Иван", surname="Иванов", phone="+375291234567",
                       email="i@example.com", average_score=4.5, scholarship=True)

    issue = ReceivingBooks(book=book, student=student, date_of_issue=datetime.now())

    session.add_all([author, book, student, issue])
    session.commit()

    # 🔥 ТЕСТ СВЯЗЕЙ
    print(f"Книги автора: {len(author.books)}")  # 1
    print(f"Автор книги: {book.author.surname}")  # Толстой
    print(f"Книги студента: {len(student.books)}")  # 1 (AssociationProxy!)
    print(f"Дней с книгой: {issue.count_date_with_book}")  # 0

    session.close()