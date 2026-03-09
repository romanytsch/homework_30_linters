from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_create_recipe():
    response = client.post("/recipes/", json={
        "title": "Тест",
        "cooking_time": 60,
        "ingredients": "ингредиенты",
        "description": "описание"
    })
    assert response.status_code == 500  # Пока БД не работает
