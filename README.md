# API Documentation

## Overview

This API provides endpoints for managing decks and cards, as well as some basic health checks and CRUD operations. 
It uses Flask for the web framework and SQLite for data storage.

## Table of Contents

1. [Health Check](#health-check)
2. [Deck and Card Endpoints](#deck-and-card-endpoints)
   - [Get Deck](#get-deckintdeck_id)
   - [Get All Decks](#get-decks)
   - [Get All Cards](#get-cards)
   - [Get Card](#get-cardintcard_id)
   - [Create Deck](#post-deck)
   - [Create Card](#post-deck)
   - [Move](#post-move)
   - [Delete](#delete-delete)
4. [Error Handling](#error-handling)
5. [To be implemented](#to-be-implemented)
6. [Deployed URL on AWS](#deployed-url-on-aws)

## Health Check

### `GET /ping`

**Description:** A health check endpoint to ensure the API is running.

**Response:**

- **200 OK**

  {
    "message": "Health Check is working"
  }

## Deck and Card Endpoints

### GET /deck/<int:deck_id>

**Description:** Retrieve a specific deck and its associated cards by deck_id.

**Description:** 

**Description:** 

    {
        "deck": [ ... ],
        "cards": [ ... ]
    }
    deck is a list of deck objects.
    cards is a list of card objects.
    404 Not Found (if the deck is not found)

## GET /decks
**Description:**  Description: Retrieve all decks.

- **200 OK**
    [
        { ... },
        { ... }
    ]

## GET /cards
**Description:**   Retrieve all cards.

- **200 OK**
    [
        { ... },
        { ... }
    ]

## GET /card/<int:card_id>
**Description:**  Retrieve a specific card by card_id.

Response:

- **200 OK**

- **404 Not Found (if the card is not found)**

## POST /deck
**Description:** Create a new deck.

Request Body:
{
  "name": "Deck Name",
  "parent_id": null // Optional
}

Response:

- **200 OK**
    {
    "status": "success"
    }


## POST /card
**Description:**  Create a new card.

Request Body:
{
  "content": "Card content",
  "deck_id": 1
}
Response:

- **200 OK**
    {
    "status": "success"
    }

## POST /move
**Description:**  Move a card or deck to a new location.

Request Body:
{
  "item_id": 1,
  "item_type": "card" or "deck",
  "target_deck_id": 2
}

Response:
- **200 OK**
{
  "status": "success"
}

## DELETE/delete
**Description:**  Delete a card or deck.

Request Body:

{
  "item_id": 1,
  "item_type": "card" or "deck"
}
Response:

- **200 OK**

{
  "status": "success"
}


### Error Handling
400 Bad Request: Indicates invalid input or parameters.
404 Not Found: Indicates that the requested resource was not found.


### To be implemented

Ordering/Position of the cards

Authentication
Rate Limits
Validation on the input , required fields
Segregation of the code , tests , more performance tests


### Deployed URL on AWS
**Example** http://3.10.199.234:5000/ping , http://3.10.199.234:5000/cards etc
**This is the URL deployed in AWS cloud and should be accessible from the Url: http://3.10.199.234:5000/**
