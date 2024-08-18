import pytest
from app import app
import json

@pytest.fixture
def client():
    return app.test_client()

def test_ping(client):
    resp = client.get('/ping')
    assert resp.json == {"message": "Health Check is working"}

def test_post(client):
    test_data = {"name" : "greeting"}
    resp = client.post('/post' , json = test_data)
    assert resp.status_code == 200 