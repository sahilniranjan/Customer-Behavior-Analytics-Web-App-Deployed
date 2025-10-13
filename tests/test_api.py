"""
Basic pytest suite for API endpoints.
"""
import pytest
from src.api.app import app, db

test_client = app.test_client()

@pytest.fixture(scope='module', autouse=True)

def setup_database():
    db.create_all()
    yield
    db.drop_all()


def test_health():
    resp = test_client.get('/health')
    assert resp.status_code == 200


def test_track_and_trends():
    # Track two events
    test_client.post('/api/track', json={'user_id':'u1','action':'click','page':'home','metadata':{}})
    test_client.post('/api/track', json={'user_id':'u2','action':'view','page':'about','metadata':{}})
    # Check trends
    resp = test_client.get('/api/analytics/trends')
    assert resp.status_code == 200
    data = resp.json['trends']
    assert isinstance(data, dict)
