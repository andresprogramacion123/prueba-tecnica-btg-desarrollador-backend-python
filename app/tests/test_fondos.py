import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app

client = TestClient(app)

# Test para obtener todos los fondos
def test_obtener_fondos():
    response = client.get("/fondos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
