import pytest


def test_create_client_factory(client):
    """ДУБЛИКАТ test_create_client с Factory Boy"""
    # Изначально пусто
    response = client.get('/clients')
    initial_count = len(response.json)

    # Создаем через API (как в оригинале)
    data = {
        "name": "Иван", "surname": "Иванов",
        "car_number": "А123БВ77", "credit_card": "4111"
    }
    resp = client.post("/clients", json=data)

    assert resp.status_code == 201
    assert len(client.get('/clients').json) == initial_count + 1
