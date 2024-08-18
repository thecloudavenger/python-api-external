from flask import Flask, request , jsonify
import sqlite3
from datetime import datetime
import os

#This was run only once
def create_db():
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()

    connection.commit()
    connection.close()
    
app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def print_health_check():
    create_db()
    return jsonify({"message": "Health Check is working"})

@app.route('/post', methods=['POST'])
def post_test():
    data = request.json
    if "name" in data and data["name"] == "greeting":
        return jsonify({"message": "Greeting received"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400
    
def execute_query(query, params=()):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

@app.route('/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM card WHERE card_id = ?', (card_id,))
    card = c.fetchone()

    conn.close()

    if card:
        return jsonify(dict(card))
    else:
        return jsonify({"error": "Card not found"}), 404


@app.route('/deck/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''
        SELECT * FROM deck WHERE deck_id = ? OR parent_id = ?;
    ''', (deck_id, deck_id))
    decks = c.fetchall()

    c.execute('''
        SELECT * FROM card WHERE deck_id = ?;
    ''', (deck_id,))
    cards = c.fetchall()

    conn.close()

    deck_data = {
        "deck": [dict(deck) for deck in decks],
        "cards": [dict(card) for card in cards]
    }

    return jsonify(deck_data)


@app.route('/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM card WHERE card_id = ?', (card_id,))
    card = c.fetchone()

    conn.close()

    if card:
        return jsonify(dict(card))
    else:
        return jsonify({"error": "Card not found"}), 404

@app.route('/move', methods=['POST'])
def move_item():
    data = request.json
    item_id = data['item_id']
    item_type = data['item_type']
    target_deck_id = data['target_deck_id']

    if item_type == 'card':
        execute_query('''
            UPDATE card
            SET deck_id = ?, updated_timestamp = ?
            WHERE card_id = ?;
        ''', (target_deck_id, datetime.now(), item_id))

    elif item_type == 'deck':
        execute_query('''
            UPDATE deck
            SET parent_id = ?, updated_timestamp = ?
            WHERE deck_id = ?;
        ''', (target_deck_id, datetime.now(), item_id))
    
    return jsonify({"status": "success"})


@app.route('/deck', methods=['POST'])
def create_deck():
    data = request.json
    name = data['name']
    parent_id = data.get('parent_id', None)

    execute_query('''
        INSERT INTO deck (name, parent_id) VALUES (?, ?)
    ''', (name, parent_id))

    return jsonify({"status": "success"})

@app.route('/card', methods=['POST'])
def create_card():
    data = request.json
    content = data['content']
    deck_id = data['deck_id']

    execute_query('''
        INSERT INTO card (content, deck_id) VALUES (?, ?)
    ''', (content, deck_id))

    return jsonify({"status": "success"})


@app.route('/delete', methods=['DELETE'])
def delete_item():
    data = request.json
    item_id = data['item_id']
    item_type = data['item_type']

    if item_type == 'card':
        execute_query('DELETE FROM card WHERE card_id = ?', (item_id,))
    elif item_type == 'deck':
        # Delete the deck and all nested decks and cards
        execute_query('DELETE FROM deck WHERE deck_id = ? OR parent_id = ?', (item_id, item_id))
        execute_query('DELETE FROM card WHERE deck_id = ?', (item_id,))

    return jsonify({"status": "success"})

if __name__== "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8081)