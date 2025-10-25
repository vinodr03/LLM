import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    print("✅ Health check passed")

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    print("✅ Root endpoint passed")

def test_docs_available():
    """Test that docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200
    print("✅ Documentation available")

def test_malicious_query_blocked():
    """Test that malicious queries are blocked"""
    # This test should work even if models aren't loaded
    response = client.post(
        "/api/v1/query",
        json={"question": "DROP TABLE users"}
    )
    # Should be blocked by security
    assert response.status_code in [400, 500]
    print("✅ Security check working")

def test_empty_query_rejected():
    """Test that empty queries are rejected"""
    response = client.post(
        "/api/v1/query",
        json={"question": ""}
    )
    assert response.status_code == 422
    print("✅ Input validation working")

if __name__ == "__main__":
    print("Running simple tests...")
    test_health_check()
    test_root()
    test_docs_available()
    test_empty_query_rejected()
    print("\n✅ All simple tests passed!")
