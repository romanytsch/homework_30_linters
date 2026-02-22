from flask import Flask, request, jsonify
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

WSGIRequestHandler.protocol_version = "HTTP/1.1"

BOOKS = []


@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(BOOKS)


@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Invalid data"}), 400

    book = {
        "id": len(BOOKS) + 1,
        "title": data["title"],
        "author": data["author"],
    }
    BOOKS.append(book)
    return jsonify(book), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
