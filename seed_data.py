import sys
from datetime import datetime, timezone
from app.database import SessionLocal, engine
from app import models, utils

def seed():
    print("[+] Seeding RentSphere database with realistic campus & city data...")
    db = SessionLocal()

    try:
        # 1. Create or get Users
        users_data = [
            {
                "email": "demo@rentsphere.com",
                "password": utils.hash("Demo@12345"),
                "phone_number": "+91 9883913522",
                "city": "Durgapur"
            },
            {
                "email": "rahul.sen@nitdgp.ac.in",
                "password": utils.hash("Rahul@123"),
                "phone_number": "+91 9831001122",
                "city": "Durgapur"
            },
            {
                "email": "priya.das@nitdgp.ac.in",
                "password": utils.hash("Priya@123"),
                "phone_number": "+91 9832003344",
                "city": "Durgapur"
            },
            {
                "email": "kolkata.pg@rentsphere.com",
                "password": utils.hash("Kolkata@123"),
                "phone_number": "+91 9830556677",
                "city": "Kolkata"
            },
            {
                "email": "arjun.tech@gmail.com",
                "password": utils.hash("Arjun@123"),
                "phone_number": "+91 9876543210",
                "city": "Kolkata"
            }
        ]

        users_dict = {}
        for u in users_data:
            existing = db.query(models.User).filter(models.User.email == u["email"]).first()
            if not existing:
                user_obj = models.User(**u)
                db.add(user_obj)
                db.commit()
                db.refresh(user_obj)
                users_dict[u["email"]] = user_obj
                print(f"  [OK] Created user: {u['email']}")
            else:
                users_dict[u["email"]] = existing

        demo_user = users_dict["demo@rentsphere.com"]
        rahul = users_dict["rahul.sen@nitdgp.ac.in"]
        priya = users_dict["priya.das@nitdgp.ac.in"]
        kolkata_mgr = users_dict["kolkata.pg@rentsphere.com"]
        arjun = users_dict["arjun.tech@gmail.com"]

        # 2. Seed realistic rooms
        rooms_data = [
            {
                "title": "Spacious 1 BHK near NIT Durgapur Main Gate",
                "description": "5 mins walk to NIT DGP main campus gate. High-speed 100Mbps fiber wifi, study table, geyser, refrigerator, and 24/7 water supply. Ideal for 2nd/3rd year engineering students.",
                "city": "Durgapur",
                "rent_amount": 5500,
                "room_type": "single",
                "is_available": True,
                "owner_id": rahul.id
            },
            {
                "title": "2-Sharing AC Flat in B-Zone near A-Zone Market",
                "description": "Fully furnished double room in B-Zone green sector. Air conditioned, inverter backup during monsoon, daily maid service, balcony overlooking the park. Walking distance to food street.",
                "city": "Durgapur",
                "rent_amount": 3800,
                "room_type": "shared",
                "is_available": True,
                "owner_id": rahul.id
            },
            {
                "title": "Quiet Study-Friendly Single Room near Muchipara Junction",
                "description": "Peaceful neighborhood with zero traffic noise. Perfect for semester exams & GATE preparation. Includes wooden bed, mattress, bookshelf, and private attached washroom.",
                "city": "Durgapur",
                "rent_amount": 4500,
                "room_type": "single",
                "is_available": True,
                "owner_id": priya.id
            },
            {
                "title": "Premium Master Suite near City Centre Durgapur",
                "description": "Located behind Junction Mall. King sized bed, modular kitchen access, covered two-wheeler parking, gated security guards, and gym nearby. Directly connected to NH-19.",
                "city": "Durgapur",
                "rent_amount": 7500,
                "room_type": "single",
                "is_available": True,
                "owner_id": priya.id
            },
            {
                "title": "Tech Hub Studio near Salt Lake Sector V Metro",
                "description": "Walkable to Wipro & DLF tech parks. Fully air-conditioned, elevator, security camera surveillance, high-speed WiFi, laundry facilities included. Ideal for tech interns.",
                "city": "Kolkata",
                "rent_amount": 9500,
                "room_type": "single",
                "is_available": True,
                "owner_id": kolkata_mgr.id
            },
            {
                "title": "Twin Sharing Room in New Town Action Area 1",
                "description": "Opposite Candor TechSpace. Twin beds, wardrobes, shared kitchen with microwave & water purifier, twice-weekly cleaning. Metro station 300 meters away.",
                "city": "Kolkata",
                "rent_amount": 6000,
                "room_type": "shared",
                "is_available": True,
                "owner_id": kolkata_mgr.id
            },
            {
                "title": "Cozy Independent Flat near Jadavpur 8B Bus Stand",
                "description": "Close to Jadavpur University and South City Mall. Independent terrace access, bright natural sunlight, well-ventilated, low electricity tariff. Friendly landlord.",
                "city": "Kolkata",
                "rent_amount": 8000,
                "room_type": "single",
                "is_available": True,
                "owner_id": kolkata_mgr.id
            },
            {
                "title": "Budget Flatmate Wanted near Ruby EM Bypass",
                "description": "Looking for a chilled flatmate in a 3BHK flat. Clean society, swimming pool, badminton court, continuous water, 24/7 security. Split expenses equally.",
                "city": "Kolkata",
                "rent_amount": 5000,
                "room_type": "shared",
                "is_available": True,
                "owner_id": arjun.id
            }
        ]

        created_rooms = []
        for r in rooms_data:
            existing_room = db.query(models.Room).filter(
                models.Room.title == r["title"],
                models.Room.owner_id == r["owner_id"]
            ).first()
            if not existing_room:
                room_obj = models.Room(**r)
                db.add(room_obj)
                db.commit()
                db.refresh(room_obj)
                created_rooms.append(room_obj)
                print(f"  [OK] Created room: {r['title']}")
            else:
                created_rooms.append(existing_room)

        # 3. Seed Reviews
        reviews_data = [
            {
                "room_id": created_rooms[0].id,
                "user_id": priya.id,
                "rating": 5,
                "comment": "Lived here during 3rd sem! Rahul bhaiya is a fantastic landlord. WiFi speed never drops even during exams."
            },
            {
                "room_id": created_rooms[0].id,
                "user_id": arjun.id,
                "rating": 5,
                "comment": "Super convenient location. 5 mins walk to NIT DGP main gate saves so much commute time."
            },
            {
                "room_id": created_rooms[1].id,
                "user_id": demo_user.id,
                "rating": 4,
                "comment": "Very peaceful B-zone sector. The AC works great during summer heat. Maid service is punctual."
            },
            {
                "room_id": created_rooms[2].id,
                "user_id": rahul.id,
                "rating": 5,
                "comment": "Total silence for studying. Attached washroom is sparkling clean."
            },
            {
                "room_id": created_rooms[4].id,
                "user_id": arjun.id,
                "rating": 5,
                "comment": "Best PG in Sector V for tech interns! Literally 3 mins walk to office."
            },
            {
                "room_id": created_rooms[5].id,
                "user_id": priya.id,
                "rating": 4,
                "comment": "Spacious twin sharing room. Good food options right outside the building."
            }
        ]

        for rev in reviews_data:
            existing_rev = db.query(models.Review).filter(
                models.Review.room_id == rev["room_id"],
                models.Review.user_id == rev["user_id"]
            ).first()
            if not existing_rev:
                r_obj = models.Review(**rev)
                db.add(r_obj)
                db.commit()
                print(f"  [OK] Added review for room {rev['room_id']}")

        # 4. Seed Bookmarks
        bookmarks_data = [
            (demo_user.id, created_rooms[0].id),
            (demo_user.id, created_rooms[4].id),
            (priya.id, created_rooms[0].id),
            (priya.id, created_rooms[1].id),
            (arjun.id, created_rooms[4].id),
            (arjun.id, created_rooms[5].id),
            (rahul.id, created_rooms[2].id),
            (rahul.id, created_rooms[6].id),
        ]

        for u_id, r_id in bookmarks_data:
            existing_bm = db.query(models.Bookmark).filter(
                models.Bookmark.user_id == u_id,
                models.Bookmark.room_id == r_id
            ).first()
            if not existing_bm:
                bm_obj = models.Bookmark(user_id=u_id, room_id=r_id)
                db.add(bm_obj)
                db.commit()
                print(f"  [OK] Added bookmark: user {u_id} -> room {r_id}")

        print("\n[SUCCESS] Database seeding complete! Total active rooms, reviews, and bookmarks are ready.")

    except Exception as e:
        print(f"[ERROR] while seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
