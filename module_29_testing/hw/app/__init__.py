from flask import Flask
from .database import db
from .models import *


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Отложенная инициализация (init_app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
