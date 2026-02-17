from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import InputRequired


class BookForm(FlaskForm):
    book_title = StringField('Book title', validators=[InputRequired()])
    author_name = StringField('Author ful name', validators=[InputRequired()])
    submit = SubmitField('Add new book')