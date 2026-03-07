import pytest
import time


@pytest.mark.parking
def test_enter_parking(client):
    c_resp = client.post("/clients", json={
        "name": "Петр", "surname": "Петров",
        "car_number": "Б456ВВ78", "credit_card": "1234"
    })
    p_resp = client.post("/parkings", json={
        "address": "Тест", "count_places": 5
    })

    enter_data = {
        "client_id": c_resp.json["id"],
        "parking_id": p_resp.json["id"]
    }

    response = client.post("/client_parkings", json=enter_data)
    assert response.status_code == 200


@pytest.mark.parking
def test_exit_parking(client):
    c_resp = client.post("/clients", json={
        "name": "Сидр", "surname": "Сидоров",
        "car_number": "В789ГГ79", "credit_card": "4321"
    })
    p_resp = client.post("/parkings", json={
        "address": "Парк", "count_places": 10
    })

    enter_data = {
        "client_id": c_resp.json["id"],
        "parking_id": p_resp.json["id"]
    }

    client.post("/client_parkings", json=enter_data)
    time.sleep(0.1)
    response = client.delete("/client_parkings", json=enter_data)
    assert response.status_code == 200
