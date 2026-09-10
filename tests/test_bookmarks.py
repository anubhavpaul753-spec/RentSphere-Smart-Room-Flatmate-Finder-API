import pytest

def test_bookmark_unauthorized(client):
    res = client.post("/bookmarks/1")
    assert res.status_code == 401

def test_bookmark_nonexistent_room(client, auth_headers):
    res = client.post("/bookmarks/999999", headers=auth_headers)
    assert res.status_code == 404

def test_bookmark_toggle_flow(client, auth_headers):
    # Fetch an existing room
    rooms_res = client.get("/rooms/?limit=1")
    assert rooms_res.status_code == 200
    rooms = rooms_res.json()
    assert len(rooms) > 0
    room_id = rooms[0]["Room"]["id"]

    # Toggle 1: Add or ensure bookmarked
    res1 = client.post(f"/bookmarks/{room_id}", headers=auth_headers)
    assert res1.status_code in [200, 201]
    data1 = res1.json()
    assert "bookmarked" in data1

    # Toggle 2: Should flip state
    res2 = client.post(f"/bookmarks/{room_id}", headers=auth_headers)
    assert res2.status_code in [200, 201]
    data2 = res2.json()
    assert data2["bookmarked"] != data1["bookmarked"]

def test_get_my_bookmarks(client, auth_headers):
    res = client.get("/bookmarks/me", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
