from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_recipe():
    response = client.post("/recipes/", json={
        "title": "Тест", "cooking_time": 60,
        "ingredients": "ингредиенты", "description": "описание"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Тест"
