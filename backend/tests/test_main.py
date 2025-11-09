# backend/tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data

def test_list_complaints():
    response = client.get("/api/v1/complaints/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)