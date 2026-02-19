from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import get_book_by_title, Book, get_author_id_by_id


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title):
            raise ValidationError('Book with this title already exists.')

    @validates('author_id')
    def validate_author_id(self, author_id: int) -> None:
        if not get_author_id_by_id(author_id):
            raise ValidationError('Author with this ID does not exist.')

    @post_load
    def create_book(self, data: dict) -> Book:
        return Book(**data)
