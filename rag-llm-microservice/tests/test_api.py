import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_normal_query():
    response = client.post(
        "/api/v1/query",
        json={"question": "What is machine learning?"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()

def test_malicious_query():
    response = client.post(
        "/api/v1/query",
        json={"question": "DROP TABLE users"}
    )
    assert response.status_code == 400

def test_empty_query():
    response = client.post(
        "/api/v1/query",
        json={"question": ""}
    )
    assert response.status_code == 422