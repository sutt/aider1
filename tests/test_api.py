# use these if running "$pytest tests/"
# don't need them if running "$PYTHONPATH=. pytest tests/"
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api import app
from src.database import Base, get_db
from src.models import FactorialResult

import uuid

# Create temporary test database name
TEST_DB_NAME = f"test_db_{uuid.uuid4().hex}"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:demopassword@localhost:5433/{TEST_DB_NAME}"

# Create test database
temp_engine = create_engine("postgresql://postgres:demopassword@localhost:5433/postgres")
with temp_engine.connect() as conn:
    conn.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
    conn.execute(f"CREATE DATABASE {TEST_DB_NAME}")
    conn.commit()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base from models to ensure all models are registered
from src.models import Base as ModelsBase

# Create test database tables
ModelsBase.metadata.drop_all(bind=engine)
ModelsBase.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

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

def test_history():
    # Clear any existing history
    db = TestingSessionLocal()
    db.query(FactorialResult).delete()
    db.commit()
    
    # Create some factorial results
    client.get("/factorial/0")
    client.get("/factorial/5")
    
    # Test history endpoint
    response = client.get("/history")
    assert response.status_code == 200
    results = response.json()
    
    # Check we have 2 results
    assert len(results) == 2
    
    # Check the results are correct
    assert results[0]["input_number"] == 0
    assert results[0]["result"] == 1
    assert results[1]["input_number"] == 5
    assert results[1]["result"] == 120

def teardown_module(module):
    """Cleanup test database after all tests complete"""
    engine.dispose()
    with temp_engine.connect() as conn:
        # Terminate all connections to the test database
        conn.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
            AND pid <> pg_backend_pid()
        """)
        conn.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        conn.commit()
    temp_engine.dispose()
