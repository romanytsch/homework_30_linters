from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_recipe():
    response = client.post(
        "/recipes/",
        json={
            "title": "Тест",
            "cooking_time": 60,
            "ingredients": "ингредиенты",
            "description": "описание",
        },
    )
    assert response.status_code == 201


def test_get_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recipe_not_found():
    response = client.get("/recipes/999")
    assert response.status_code == 404
