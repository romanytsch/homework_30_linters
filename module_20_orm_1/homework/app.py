from datetime import datetime

from flask import Flask, jsonify, request

from ORM_db import Books, ReceivingBooks, Base, engine, Students, Session

app = Flask(__name__)

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

@app.route('/debtors', methods=['GET'])
def get_debtors():
    session = Session()
    from datetime import timedelta
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


@app.route('/return_book', methods=['POST'])  # ✅ Добавлен недостающий роут
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

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
