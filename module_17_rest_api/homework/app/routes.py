from flask import Flask, request
from flask_restful import Api, Resource, abort
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_author_id,
)
from schemas import BookSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class BookResource(Resource):
    def get(self, book_id: int) -> tuple[dict | None, int]:
        """GET /api/books/{id} - получить книгу по ID"""
        book = get_book_by_id(book_id)
        if not book:
            abort(404, message="Book not found")

        schema = BookSchema()
        return schema.dump(book), 200

    def put(self, book_id: int) -> tuple[dict, int]:
        """PUT /api/books/{id} - полностью заменить книгу"""
        data = request.json
        schema = BookSchema()

        try:
            new_book_data = schema.load(data)
            new_book_data.id = book_id  # Фиксируем ID

            # Проверяем существование книги
            if not get_book_by_id(book_id):
                return {"message": "Book not found"}, 404

            update_book_by_id(new_book_data)
            updated_book = get_book_by_id(book_id)
            return schema.dump(updated_book), 200

        except ValidationError as exc:
            return exc.messages, 400

    def delete(self, book_id: int) -> tuple[dict, int]:
        """DELETE /api/books/{id} - удалить книгу"""
        if not get_book_by_id(book_id):
            return {"message": "Book not found"}, 404

        delete_book_by_id(book_id)
        return {"message": "Book deleted"}, 200


# Регистрируем ресурсы
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
