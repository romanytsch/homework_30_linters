from marshmallow import Schema, fields, validates, ValidationError, post_load
import sqlite3
from models import Book, Author, get_book_by_title, get_author_id_by_id, get_author_by_id

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False, allow_none=True)

    @post_load
    def create_author(self, data: dict) -> Author:
        return Author(**data)

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
