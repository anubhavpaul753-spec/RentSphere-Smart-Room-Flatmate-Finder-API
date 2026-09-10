import pytest

def test_get_rooms_list(client):
    res = client.get("/rooms/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    if len(data) > 0:
        room_item = data[0]
        assert "Room" in room_item
        assert "bookmarks" in room_item
        assert "avg_rating" in room_item

def test_get_rooms_filter_city(client):
    res = client.get("/rooms/?city=Durgapur")
    assert res.status_code == 200
    data = res.json()
    for item in data:
        assert "durgapur" in item["Room"]["city"].lower()

def test_create_room_unauthorized(client):
    res = client.post("/rooms/", json={
        "title": "Unauthorized Listing",
        "description": "Should fail without auth",
        "city": "Durgapur",
        "rent_amount": 4000,
        "room_type": "single",
        "is_available": True
    })
    assert res.status_code == 401

def test_create_and_delete_room(client, auth_headers):
    # 1. Create Room
    create_res = client.post("/rooms/", headers=auth_headers, json={
        "title": "Pytest Automated Room Listing",
        "description": "Created during automated testing",
        "city": "Durgapur",
        "rent_amount": 4200,
        "room_type": "single",
        "is_available": True
    })
    assert create_res.status_code == 201
    room_data = create_res.json()
    room_id = room_data["id"]

    # 2. Get Single Room
    get_res = client.get(f"/rooms/{room_id}")
    assert get_res.status_code == 200
    assert get_res.json()["Room"]["title"] == "Pytest Automated Room Listing"

    # 3. Delete Room (Authorized)
    del_res = client.delete(f"/rooms/{room_id}", headers=auth_headers)
    assert del_res.status_code == 204
