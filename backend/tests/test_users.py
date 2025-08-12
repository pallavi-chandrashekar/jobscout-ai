def test_create_user(client):
    response = client.post("/users/", json={"email": "test@example.com", "name": "Test User"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
