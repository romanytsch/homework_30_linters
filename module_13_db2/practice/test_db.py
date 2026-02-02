from datetime import datetime, timedelta
from sqlalchemy import (Table, create_engine, Column, Integer, String, Date,
                        MetaData, Float, Boolean, DateTime)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask, jsonify, request

app = Flask(__name__)

engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    surname = Column(String(16), nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    surname = Column(String(16), nullable=False)
    phone = Column(String(16), nullable=False)
    email = Column(String(16), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_scholarship_students(cls):
        return session.query(cls).filter(cls.scholarship == True).all()

    @classmethod
    def get_high_score_students(cls, min_score):
        return session.query(cls).filter(cls.average_score > min_score).all()



class Receiving_books(Base):
    __tablename__ = 'receiving_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, nullable=True)


    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @hybrid_property
    def count_date_with_book(self):
        """Количество дней, которые читатель держит/держал книгу у себя"""
        if self.date_of_return is None:
            # Если книгу не сдали, считаем до текущей даты
            return (datetime.now() - self.date_of_issue).days
        else:
            # Если сдали, считаем разницу между датами выдачи и возврата
            return (self.date_of_return - self.date_of_issue).days


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)

@app.route('/')
def hello_world():
    return 'Hello World!'


## GET /books - все книги
@app.route('/books', methods=['GET'])
def get_all_books():
    """Получить все книги в библиотеке"""
    books = session.query(Books).all()
    return jsonify([book.to_json() for book in books])


## GET /debtors - должники > 14 дней
@app.route('/debtors', methods=['GET'])
def get_debtors():
    """Список должников, держащих книги > 14 дней"""

    fourteen_days_ago = datetime.now() - timedelta(days=14)

    debtors = session.query(Receiving_books) \
        .filter(
        Receiving_books.date_of_return.is_(None),
        Receiving_books.date_of_issue < fourteen_days_ago
    ).all()

    result = []
    for record in debtors:
        record_data = record.to_json()
        record_data['days_overdue'] = (datetime.now() - record.date_of_issue).days
        result.append(record_data)

    return jsonify(result)


## POST /issue-book - выдать книгу
@app.route('/issue-book', methods=['POST'])
def issue_book():
    """Выдать книгу студенту (book_id, student_id)"""
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'Требуются book_id и student_id'}), 400

    with Session() as session:
        # Проверяем существование
        book = session.query(Books).filter(Books.id == book_id).first()
        student = session.query(Students).filter(Students.id == student_id).first()

        if not book or not student:
            return jsonify({'error': 'Книга или студент не найдены'}), 404

        # Создаем запись выдачи
        record = Receiving_books(
            book_id=book_id,
            student_id=student_id,
            date_of_issue=datetime.now()
        )
        session.add(record)
        session.commit()

        return jsonify({
            'message': 'Книга выдана',
            'record_id': record.id,
            'issue_date': record.date_of_issue.isoformat()
        }), 201


## POST /return-book - сдать книгу
@app.route('/return-book', methods=['POST'])
def return_book():
    """Сдать книгу (book_id, student_id). Ошибка если связки нет"""
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'Требуются book_id и student_id'}), 400

    with Session() as session:
        # Ищем активную выдачу (не сданную)
        record = session.query(Receiving_books) \
            .filter(
            Receiving_books.book_id == book_id,
            Receiving_books.student_id == student_id,
            Receiving_books.date_of_return.is_(None)
        ).first()

        if not record:
            return jsonify({'error': 'Активная выдача не найдена'}), 404

        # Сдаём книгу
        record.date_of_return = datetime.now()
        session.commit()

        days_held = (record.date_of_return - record.date_of_issue).days

        return jsonify({
            'message': 'Книга сдана',
            'record_id': record.id,
            'return_date': record.date_of_return.isoformat(),
            'days_held': days_held
        })


if __name__ == '__main__':
    app.run()