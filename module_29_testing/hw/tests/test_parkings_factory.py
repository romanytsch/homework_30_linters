import pytest


def test_create_parking_factory(client):
    """ДУБЛИКАТ test_create_parking"""
    data = {"address": "ул. Тестовая 1", "count_places": 10}
    resp = client.post("/parkings", json=data)
    assert resp.status_code == 201  # ✅ Основная проверка
