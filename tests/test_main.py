import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import main

client = TestClient(main.app)

@pytest.fixture
def mock_db():
    with patch('main.SessionLocal'):
        yield

def test_create_recipe(mock_db):
    response = client.post("/recipes/", json={
        "title": "Тест",
        "cooking_time": 60,
        "ingredients": "ингредиенты",
        "description": "описание"
    })
    assert response.status_code == 201
