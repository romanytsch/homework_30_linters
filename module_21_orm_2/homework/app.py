import csv
import io
import os
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from sqlalchemy import func, and_
from werkzeug.utils import secure_filename

from ORM_db import Books, ReceivingBooks, Base, engine, Students, Session, Authors

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/upload_students', methods=['POST'])
def upload_students():
    """Загрузка CSV студентов в базу"""
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не найден'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Требуется CSV файл'}), 400

    session = Session()

    try:
        # Читаем CSV
        file.stream.seek(0)
        text_stream = io.TextIOWrapper(file.stream, encoding='utf-8')
        reader = csv.DictReader(text_stream, delimiter=';')

        required_fields = {'name', 'surname', 'phone', 'email', 'average_score', 'scholarship'}
        if not required_fields.issubset(reader.fieldnames):
            return jsonify({'error': f'Отсутствуют поля: {required_fields - set(reader.fieldnames)}'}), 400

        # Создаем и добавляем студентов
        students_added = 0
        for row_num, row in enumerate(reader, 1):
            try:
                student = Students(
                    name=row['name'].strip(),
                    surname=row['surname'].strip(),
                    phone=row['phone'].strip(),
                    email=row['email'].strip(),
                    average_score=float(row['average_score']),
                    scholarship=row['scholarship'].lower() in ('true', '1', 'yes', 'да')
                )
                session.add(student)
                students_added += 1
            except (ValueError, KeyError) as e:
                print(f"Ошибка в строке {row_num}: {e}")  # Логируем, но продолжаем
                continue

        if students_added == 0:
            return jsonify({'error': 'Нет данных для загрузки'}), 400

        session.commit()
        print(f"Добавлено {students_added} студентов")  # Лог в консоль

        return jsonify({
            'message': f'Загружено: {students_added} студентов',
            'count': students_added
        }), 201

    except Exception as e:
        session.rollback()
        print(f"ОШИБКА: {e}")
        return jsonify({'error': f'Ошибка обработки: {str(e)}'}), 400
    finally:
        session.close()


@app.route('/debtors', methods=['GET'])
def get_debtors():
    session = Session()
    overdue = session.query(ReceivingBooks).filter(
        ReceivingBooks.date_of_return.is_(None),
        ReceivingBooks.date_of_issue < datetime.now() - timedelta(days=14)
    ).all()
    result = []
    for rb in overdue:
        student = session.query(Students).get(rb.student_id)
        book = session.query(Books).get(rb.book_id)
        result.append({
            'student': f"{student.name} {student.surname}",
            'book': book.name,
            'days': (datetime.now() - rb.date_of_issue).days
        })
    session.close()
    return jsonify(result)

@app.route('/books', methods=['GET'])
def get_all_books():
    session = Session()
    books = session.query(Books).all()
    result = [{'id': book.id,
               'name': book.name,
               'count': book.count,
               'release_date': book.release_date.isoformat()} for book in books]
    session.close()
    return jsonify(result)

@app.route('/students', methods=['GET'])
def get_all_students():
    """Получить всех студентов"""
    session = Session()
    students = session.query(Students).all()
    result = [{'id': s.id,
               'name': f"{s.name} {s.surname}",
               'phone': s.phone,
               'email': s.email,
               'average_score': s.average_score,
               'scholarship': s.scholarship}
              for s in students]
    session.close()
    return jsonify(result)

@app.route('/issue_book', methods=['POST'])
def issue_book():
    data = request.json
    session = Session()
    issue = ReceivingBooks(
        book_id=data['book_id'],
        student_id=data['student_id'],
        date_of_issue=datetime.now()
    )
    session.add(issue)
    session.commit()
    session.close()
    return jsonify({'message': 'Книга выдана'}), 201


@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.json
    session = Session()
    issue = session.query(ReceivingBooks).filter_by(
        book_id=data['book_id'],
        student_id=data['student_id'],
        date_of_return=None
    ).first()

    if not issue:
        session.close()
        return jsonify({'error': 'Связка книга-студент не найдена или книга уже сдана'}), 404

    issue.date_of_return = datetime.now()
    session.commit()
    session.close()
    return jsonify({'message': 'Книга сдана'})


# НОВЫЕ РОУТЫ:

@app.route('/author_books_count/<int:author_id>', methods=['GET'])
def author_books_count(author_id):
    """1. Кол-во оставшихся книг по автору"""
    session = Session()
    total_count = session.query(func.sum(Books.count)).filter(
        Books.author_id == author_id
    ).scalar() or 0

    issued_count = session.query(func.count(ReceivingBooks.id)).join(Books).filter(
        and_(Books.author_id == author_id, ReceivingBooks.date_of_return.is_(None))
    ).scalar()

    available = total_count - issued_count
    session.close()
    return jsonify({'author_id': author_id, 'available_books': available})


@app.route('/student_unread_books/<int:student_id>', methods=['GET'])
def student_unread_books(student_id):
    """2. Книги автора, которые студент НЕ читал (но другие книги автора читал)"""
    session = Session()

    # Авторы, книги которых студент брал
    read_authors = session.query(Authors.id).join(Books).join(ReceivingBooks).filter(
        ReceivingBooks.student_id == student_id
    ).distinct().all()

    read_author_ids = [author_id for (author_id,) in read_authors]

    if not read_author_ids:
        session.close()
        return jsonify({'message': 'Студент не читал книг'})

    # Книги этих авторов, которые студент НЕ брал
    unread_books = session.query(Books).filter(
        and_(
            Books.author_id.in_(read_author_ids),
            ~Books.id.in_(
                session.query(ReceivingBooks.book_id).filter(
                    ReceivingBooks.student_id == student_id
                )
            )
        )
    ).all()

    result = [{'id': b.id, 'name': b.name,
               'author': f"{b.author.name} {b.author.surname}"} for b in unread_books]
    session.close()
    return jsonify(result)


@app.route('/avg_books_this_month', methods=['GET'])
def avg_books_this_month():
    """3. Среднее кол-во книг в этом месяце"""
    session = Session()
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    subquery = session.query(
        ReceivingBooks.student_id,
        func.count(ReceivingBooks.id).label('books_count')
    ).filter(
        ReceivingBooks.date_of_issue >= month_start
    ).group_by(ReceivingBooks.student_id).subquery()

    avg = session.query(func.avg(subquery.c.books_count)).scalar() or 0
    session.close()
    return jsonify({'average_books_per_student': round(float(avg), 2)})


@app.route('/most_popular_high_score_book', methods=['GET'])
def most_popular_high_score_book():
    """4. Самая популярная книга среди отличников (>4.0)"""
    session = Session()

    popular_book = session.query(
        Books.id, Books.name, func.count(ReceivingBooks.id).label('issues')
    ).join(ReceivingBooks).join(Students).filter(
        Students.average_score > 4.0
    ).group_by(Books.id, Books.name).order_by(
        func.count(ReceivingBooks.id).desc()
    ).first()

    if popular_book:
        result = {
            'book_id': popular_book.id,
            'book_name': popular_book.name,
            'issues_count': popular_book.issues
        }
    else:
        result = {'message': 'Нет данных'}

    session.close()
    return jsonify(result)


@app.route('/top_reading_students_year', methods=['GET'])
def top_reading_students_year():
    """5. ТОП-10 студентов по книгам в этом году"""
    session = Session()
    year_start = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    top_students = session.query(
        Students.id,
        func.concat(Students.name, ' ', Students.surname).label('full_name'),
        func.count(ReceivingBooks.id).label('books_count')
    ).join(ReceivingBooks).filter(
        ReceivingBooks.date_of_issue >= year_start
    ).group_by(Students.id, Students.name, Students.surname).order_by(
        func.count(ReceivingBooks.id).desc()
    ).limit(10).all()

    result = [{'id': s.id, 'name': s.full_name, 'books_count': s.books_count}
              for s in top_students]
    session.close()
    return jsonify(result)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': '📚 Библиотека API v1.0',
        'status': 'online',
        'routes': [
            'GET /books',
            'GET /students',
            'GET /debtors',
            'POST /upload_students',
            'POST /issue_book'
        ]
    })

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
