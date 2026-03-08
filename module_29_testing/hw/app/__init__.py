from flask import Flask
from .database import db
from .models import *


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Регистрация API роутов
    from .api import api_bp
    app.register_blueprint(api_bp)

    return app

