"""
Unit tests for API endpoints
"""

import pytest
from backend.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app('testing')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200


def test_register_missing_fields(client):
    """Test register with missing fields"""
    response = client.post('/api/auth/register', json={})
    assert response.status_code == 400


# Add more tests as needed