import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base, RecipeDB, SQLALCHEMY_DATABASE_URL

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_recipes.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_create_recipe(client):
    response = client.post(
        "/recipes/",
        json={
            "title": "Тестовый суп",
            "cooking_time": 30,
            "ingredients": "вода, картошка",
            "description": "Простой суп"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовый суп"
    assert data["cooking_time"] == 30


def test_get_recipes(client):
    # Создаем рецепт
    client.post(
        "/recipes/",
        json={
            "title": "Суп",
            "cooking_time": 30,
            "ingredients": "вода",
            "description": "Тест"
        },
    )
    response = client.get("/recipes/")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["title"] == "Суп"


def test_get_recipe_not_found(client):
    response = client.get("/recipes/999")
    assert response.status_code == 404
