import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base, SQLALCHEMY_DATABASE_URL
from unittest.mock import patch

# Тестовый клиент
client = TestClient(app)

# Тестовая БД
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_recipes.db"
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Dependency override для тестов
def override_get_db():
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_create_recipe():
    response = client.post(
        "/recipes/",
        json={
            "title": "Тестовый борщ",
            "cooking_time": 120,
            "ingredients": "свёкла, капуста, картошка",
            "description": "Классический украинский борщ"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовый борщ"
    assert data["cooking_time"] == 120

def test_get_recipes():
    # Создаём рецепт
    client.post(
        "/recipes/",
        json={
            "title": "Плов",
            "cooking_time": 90,
            "ingredients": "рис, мясо, морковь",
            "description": "Узбекский плов"
        },
    )
    
    response = client.get("/recipes/")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["title"] == "Плов"

def test_get_recipe_detail_not_found():
    response = client.get("/recipes/999")
    assert response.status_code == 404
