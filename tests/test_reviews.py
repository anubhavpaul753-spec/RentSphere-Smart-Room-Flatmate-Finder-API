import pytest

def test_review_unauthorized(client):
    res = client.post("/reviews/1", json={"rating": 5, "comment": "Test without token"})
    assert res.status_code == 401

def test_review_rating_bounds(client, auth_headers):
    # Fetch an existing room
    rooms = client.get("/rooms/?limit=1").json()
    room_id = rooms[0]["Room"]["id"]

    # Rating 0 should fail
    res_low = client.post(f"/reviews/{room_id}", headers=auth_headers, json={"rating": 0, "comment": "Too low"})
    assert res_low.status_code == 422

    # Rating 6 should fail
    res_high = client.post(f"/reviews/{room_id}", headers=auth_headers, json={"rating": 6, "comment": "Too high"})
    assert res_high.status_code == 422

def test_review_self_room_forbidden(client, auth_headers):
    # 1. Create room as test_user
    create_room = client.post("/rooms/", headers=auth_headers, json={
        "title": "Room For Self Review Test",
        "description": "Testing landlord self-review restriction",
        "city": "Durgapur",
        "rent_amount": 5000,
        "room_type": "single",
        "is_available": True
    })
    room_id = create_room.json()["id"]

    # 2. Try to review own room
    res = client.post(f"/reviews/{room_id}", headers=auth_headers, json={
        "rating": 5,
        "comment": "I am the landlord and I love my own room!"
    })
    assert res.status_code == 400
    assert "Landlords cannot review" in res.json()["detail"]

    # Clean up room
    client.delete(f"/rooms/{room_id}", headers=auth_headers)

def test_review_create_and_update(client, secondary_auth_headers):
    # Fetch an existing room (owned by someone else)
    rooms = client.get("/rooms/?limit=5").json()
    room_id = rooms[0]["Room"]["id"]

    # 1. Submit review
    res1 = client.post(f"/reviews/{room_id}", headers=secondary_auth_headers, json={
        "rating": 4,
        "comment": "Very nice room from automated test"
    })
    assert res1.status_code in [200, 201]
    rev_id = res1.json()["id"]

    # 2. Get reviews for room
    summary = client.get(f"/reviews/{room_id}").json()
    assert summary["room_id"] == room_id
    assert summary["total_reviews"] >= 1
    assert summary["avg_rating"] >= 1.0

    # 3. Clean up review
    del_res = client.delete(f"/reviews/{rev_id}", headers=secondary_auth_headers)
    assert del_res.status_code == 204
