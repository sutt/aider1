import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_factorial_zero():
    response = client.get("/factorial/0")
    assert response.status_code == 200
    assert response.json() == {"result": 1}

def test_factorial_positive():
    response = client.get("/factorial/5")
    assert response.status_code == 200
    assert response.json() == {"result": 120}

def test_factorial_invalid_input():
    response = client.get("/factorial/abc")
    assert response.status_code == 422
    assert "detail" in response.json()
