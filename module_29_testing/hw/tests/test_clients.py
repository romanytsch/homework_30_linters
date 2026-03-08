import pytest

@pytest.mark.parametrize("endpoint", ["/clients"])
def test_get_methods(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200

def test_create_client(client):
    data = {"name": "Иван", "surname": "Иванов",
            "car_number": "А123БВ77", "credit_card": "4111"}
    response = client.post("/clients", json=data)
    assert response.status_code == 201
