def test_create_parking(client):
    data = {"address": "ул. Тест 1", "count_places": 50}
    response = client.post("/parkings", json=data)
    assert response.status_code == 201
    assert response.json["total_places"] == 50
