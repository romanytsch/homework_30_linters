from flask import Flask, request
from flask_restful import Api, Resource, abort
from marshmallow import ValidationError
import sqlite3

from models import (
    DATA, init_db, get_all_books, add_book, get_book_by_id,
    update_book_by_id, delete_book_by_id, get_book_by_title,
    add_author, get_author_by_id, get_books_by_author, get_author_id_by_id,
    Author, Book
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self):
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self):
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book = add_book(book)
        return schema.dump(book), 201


class BookResource(Resource):
    def get(self, book_id: int):
        book = get_book_by_id(book_id)
        if not book:
            abort(404, message="Book not found")
        schema = BookSchema()
        return schema.dump(book), 200

    def put(self, book_id: int):
        data = request.json
        schema = BookSchema()
        try:
            new_book_data = schema.load(data)
            new_book_data.id = book_id
            if not get_book_by_id(book_id):
                return {"message": "Book not found"}, 404
            update_book_by_id(new_book_data)
            updated_book = get_book_by_id(book_id)
            return schema.dump(updated_book), 200
        except ValidationError as exc:
            return exc.messages, 400

    def delete(self, book_id: int):
        if not get_book_by_id(book_id):
            return {"message": "Book not found"}, 404
        delete_book_by_id(book_id)
        return {"message": "Book deleted"}, 200


class AuthorList(Resource):
    def get(self):
        with sqlite3.connect('table_books.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM authors')
            authors = []
            for row in cursor.fetchall():
                author = Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])
                authors.append(author)
        return AuthorSchema().dump(authors, many=True), 200

    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return AuthorSchema().dump(author), 201


class AuthorResource(Resource):
    def get(self, author_id: int):
        if not get_author_id_by_id(author_id):
            abort(404, message="Author not found")

        books = get_books_by_author(author_id)
        return BookSchema().dump(books, many=True), 200

    def delete(self, author_id: int):
        if not get_author_id_by_id(author_id):
            return {"message": "Author not found"}, 404


        with sqlite3.connect('table_books.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM authors WHERE id = ?', (author_id,))
            conn.commit()

        return {"message": "Author and all books deleted"}, 200


api.add_resource(BookList, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
