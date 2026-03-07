import pytest
from app import create_app
from app.database import db


@pytest.fixture(scope="function")
def app():
    """Тестовое приложение - БД ИНИЦИАЛИЗИРОВАНА в create_app()"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False
    })

    # ✅ БЕЗ db.init_app(app) - уже вызвано в create_app()!
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
