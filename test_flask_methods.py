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

def test_post_card(client):
    test_data = {"content": "new_card", "deck_id": 1}
    resp = client.post('/card', json=test_data)
    assert resp.status_code == 200
    assert resp.json == {"status": "success"}

def test_get_deck(client):
    # Assuming deck 1 exists from initialization
    resp = client.get('/deck/1')
    assert resp.status_code == 200
    assert "deck" in resp.json
    assert "cards" in resp.json

def test_get_card(client):
    # Assuming card 1 exists from initialization
    resp = client.get('/card/1')
    assert resp.status_code == 200
    assert resp.json['card_id'] == 1
    assert resp.json['content'] == 'card 1'

def test_move_card(client):
    move_data = {"item_id": 1, "item_type": "card", "target_deck_id": 2}
    resp = client.post('/move', json=move_data)
    assert resp.status_code == 200
    assert resp.json == {"status": "success"}

    # Verify that the card has been moved
    resp = client.get('/deck/2')
    assert any(card['card_id'] == 1 for card in resp.json['cards'])

def test_move_deck(client):
    move_data = {"item_id": 3, "item_type": "deck", "target_deck_id": 2}
    resp = client.post('/move', json=move_data)
    assert resp.status_code == 200
    assert resp.json == {"status": "success"}

    # Verify that the deck has been moved
    resp = client.get('/deck/2')
    assert any(deck['deck_id'] == 3 for deck in resp.json['deck'])

def test_delete_card(client):
    delete_data = {"item_id": 1, "item_type": "card"}
    resp = client.delete('/delete', json=delete_data)
    assert resp.status_code == 200
    assert resp.json == {"status": "success"}

    # Verify that the card has been deleted
    resp = client.get('/card/1')
    assert resp.status_code == 404

def test_delete_deck(client):
    delete_data = {"item_id": 1, "item_type": "deck"}
    resp = client.delete('/delete', json=delete_data)
    assert resp.status_code == 200
    assert resp.json == {"status": "success"}

    # Verify that the deck has been deleted
    resp = client.get('/deck/1')
    assert resp.status_code == 200
    assert len(resp.json['deck']) == 0