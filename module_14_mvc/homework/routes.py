from flask import Flask, render_template, request, redirect, url_for
from typing import List

from models import init_db, get_all_books, DATA, add_book, get_books_by_author
from forms import BookForm

app: Flask = Flask(__name__)

app.secret_key = 'you-secret-key'


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )



@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()

    if form.validate_on_submit():
        add_book(form.book_title.data, form.author_name.data)
        return redirect(url_for('all_books'))

    return render_template('add_book.html', form=form)


@app.route('/author/<author_name>')
def books_by_author(author_name: str):
    books = get_books_by_author(author_name)
    return render_template('author_books.html',
                         books=books,
                         author=author_name)


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
