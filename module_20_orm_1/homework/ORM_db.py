from datetime import date

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, mapper, declarative_base

engine = create_engine("sqlite:///./library.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Убрал лимит 16 символов
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)  # Date вместо DateTime
    author_id = Column(Integer, nullable=False)

class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def get_scholarship_students(cls, session):
        return session.query(cls).filter_by(scholarship=True).all()

    @classmethod
    def get_high_score_students(cls, session, score):
        return session.query(cls).filter(cls.average_score > score).all()


class ReceivingBooks(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
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

    author = Authors(name="Лев", surname="Толстой")
    session.add(author)
    session.commit()

    book = Books(name="Война и мир", count=3,
                 release_date=date(1865, 1, 1), author_id=1)
    session.add(book)
    session.commit()

    student = Students(name="Иван", surname="Иванов",
                       phone="+375291234567", email="i@example.com",
                       average_score=4.5, scholarship=True)
    session.add(student)
    session.commit()

    session.close()