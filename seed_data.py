import sys
from datetime import datetime, timezone
from app.database import SessionLocal, engine
from app import models, utils

def seed():
    print("[+] Seeding RentSphere with 14 authentic, verified Durgapur & Kolkata listings...")
    db = SessionLocal()

    try:
        # 1. Create or get verified student landlords & tenants
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
                "email": "sourav.ghosh@nitdgp.ac.in",
                "password": utils.hash("Sourav@123"),
                "phone_number": "+91 9830556677",
                "city": "Durgapur"
            },
            {
                "email": "ankit.verma@gmail.com",
                "password": utils.hash("Ankit@123"),
                "phone_number": "+91 9876543210",
                "city": "Durgapur"
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
                print(f"  [OK] User ready: {u['email']}")
            else:
                users_dict[u["email"]] = existing

        demo_user = users_dict["demo@rentsphere.com"]
        rahul = users_dict["rahul.sen@nitdgp.ac.in"]
        priya = users_dict["priya.das@nitdgp.ac.in"]
        sourav = users_dict["sourav.ghosh@nitdgp.ac.in"]
        ankit = users_dict["ankit.verma@gmail.com"]

        # 2. 14 Authentic Durgapur Listings with exact proximity & real photos
        rooms_data = [
            {
                "title": "Aashirbad PG & Student Home (Fuljhore)",
                "description": "5 mins walk to NIT DGP North Gate. Includes 100 Mbps fiber wifi, wooden study desk, power backup for monsoon load-shedding, attached bathroom, and RO drinking water. Quiet environment for exam study.",
                "city": "Durgapur",
                "locality": "Fuljhore Road",
                "rent_amount": 4500,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5525,
                "longitude": 87.2975,
                "distance_campus": "🚶 350m (4 min walk) to NIT DGP North Gate",
                "distance_mall": "🎬 3.2 km to Junction Mall (City Centre)",
                "distance_market": "🛍️ 1.8 km to Benachity Market Place",
                "distance_food": "🌯 500m to Hostel Haven (Evening Food Stalls)",
                "image_url": "/static/assets/rooms/fuljhore_student_room.jpg",
                "owner_id": rahul.id
            },
            {
                "title": "B-Zone Sector 2B DSP Flat (Near Hall 7)",
                "description": "Prime B-Zone residential quarter flat directly behind NIT Hall 7. AC fitted, 2 beds, spacious balcony overlooking lush trees, daily maid service, inverter backup. Very friendly to 2nd/3rd years.",
                "city": "Durgapur",
                "locality": "B-Zone (Sector 2B)",
                "rent_amount": 3800,
                "room_type": "shared",
                "is_available": True,
                "latitude": 23.5440,
                "longitude": 87.2890,
                "distance_campus": "🚶 250m (3 min walk) to NIT West Gate & Hall 7",
                "distance_mall": "🎬 2.8 km to Junction Mall",
                "distance_market": "🛍️ 1.4 km to Benachity Shopping Street",
                "distance_food": "🍜 300m to Hostel Haven / Hall 7 Food Stalls",
                "image_url": "/static/assets/rooms/bzone_shared_room.jpg",
                "owner_id": rahul.id
            },
            {
                "title": "Manishankar Sri Krishna Kunj 1BHK (Fuljhore)",
                "description": "Modern independent 1BHK flat in a newly built gated society on Jemua Road. Modular kitchen, covered two-wheeler parking, dedicated water purifier, bright sunlight, and absolute privacy.",
                "city": "Durgapur",
                "locality": "Jemua Road, Fuljhore",
                "rent_amount": 6200,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5550,
                "longitude": 87.3010,
                "distance_campus": "🚶 600m (8 min walk) to NIT DGP Main Gate",
                "distance_mall": "🎬 3.6 km to Junction Mall",
                "distance_market": "🛍️ 2.1 km to Benachity Market",
                "distance_food": "☕ 750m to Hostel Haven & Nescafe",
                "image_url": "/static/assets/rooms/sri_krishna_kunj.jpg",
                "owner_id": priya.id
            },
            {
                "title": "Goswami Student Nest (Binapani Club, Fuljhore)",
                "description": "Ideal for GATE aspirants & researchers wanting total silence. Single room with wooden bed, foam mattress, large bookshelf, private washroom, and optional home-cooked Bengali mess meals.",
                "city": "Durgapur",
                "locality": "Fuljhore (Near Binapani Club)",
                "rent_amount": 4200,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5510,
                "longitude": 87.2960,
                "distance_campus": "🚶 280m (3 min walk) to NIT DGP North Gate",
                "distance_mall": "🎬 3.1 km to Junction Mall",
                "distance_market": "🛍️ 1.7 km to Benachity Market",
                "distance_food": "🍲 450m to Hostel Haven Food Hub",
                "image_url": "/static/assets/rooms/goswami_nest.jpg",
                "owner_id": priya.id
            },
            {
                "title": "Chandidas Avenue 2BHK Flat (Benachity Market)",
                "description": "Heart of Benachity market. Everything is 30 seconds away: fresh veggies, medical stores, fruit stalls, stationary, and street food. Flat accommodates 3-4 batchmates with spacious shared hall.",
                "city": "Durgapur",
                "locality": "Chandidas Avenue, Benachity",
                "rent_amount": 3200,
                "room_type": "shared",
                "is_available": True,
                "latitude": 23.5575,
                "longitude": 87.2825,
                "distance_campus": "🚌 1.2 km (4 min e-rickshaw) to NIT West Gate",
                "distance_mall": "🎬 2.2 km to Junction Mall",
                "distance_market": "🛍️ 50m (Directly inside Benachity Market)",
                "distance_food": "🥘 1.4 km to Hostel Haven",
                "image_url": "/static/assets/rooms/chandidas_flat.jpg",
                "owner_id": sourav.id
            },
            {
                "title": "Fortune Park Lane Master Suite (City Centre)",
                "description": "Directly behind Junction Mall. Luxury room in premium residential society with lift, 24/7 security guard, power backup, and gym nearby. Ideal for tech interns and seniors who want city perks.",
                "city": "Durgapur",
                "locality": "City Centre (Behind Junction Mall)",
                "rent_amount": 7800,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5345,
                "longitude": 87.2970,
                "distance_campus": "🚌 2.2 km (6 min auto/toto) to NIT DGP Gate",
                "distance_mall": "🎬 200m (2 min walk) to Junction Mall & Inox",
                "distance_market": "🛍️ 2.5 km to Benachity",
                "distance_food": "🍕 250m to City Centre Food Court & KFC",
                "image_url": "/static/assets/rooms/fortune_park_suite.jpg",
                "owner_id": sourav.id
            },
            {
                "title": "B-Zone Green Avenue 1BHK (Tagore School Area)",
                "description": "Peaceful residential flat in Sector 2C with independent terrace access. Surrounded by trees, zero street noise, low electricity tariff, continuous municipality water supply.",
                "city": "Durgapur",
                "locality": "B-Zone (Sector 2C)",
                "rent_amount": 5000,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5410,
                "longitude": 87.2860,
                "distance_campus": "🚶 550m (7 min walk) to NIT DGP West Gate",
                "distance_mall": "🎬 2.6 km to Junction Mall",
                "distance_market": "🛍️ 1.1 km to Benachity Market",
                "distance_food": "🥪 600m to Hostel Haven Food Stalls",
                "image_url": "/static/assets/rooms/bzone_green_avenue.jpg",
                "owner_id": ankit.id
            },
            {
                "title": "Bhiringi More Student PG (Near Benachity Entry)",
                "description": "Budget student PG right at Bhiringi junction. 2-sharing room with high-speed WiFi, twice-weekly laundry, drinking water cooler, and quick toto connectivity to campus.",
                "city": "Durgapur",
                "locality": "Bhiringi / Benachity",
                "rent_amount": 3500,
                "room_type": "shared",
                "is_available": True,
                "latitude": 23.5595,
                "longitude": 87.2870,
                "distance_campus": "🚶 900m (10 min walk) to NIT DGP North Gate",
                "distance_mall": "🎬 2.7 km to Junction Mall",
                "distance_market": "🛍️ 300m to Benachity Main Market",
                "distance_food": "🧆 1.1 km to Hostel Haven",
                "image_url": "/static/assets/rooms/bhiringi_pg.jpg",
                "owner_id": ankit.id
            },
            {
                "title": "Jemua Horizon 2BHK (Fuljhore Extension)",
                "description": "Spacious flat for a group of 3-4 engineering students. Large study hall with whiteboard, balcony facing greenery, motorbike parking, and clean drinking water.",
                "city": "Durgapur",
                "locality": "Fuljhore (Jemua Horizon)",
                "rent_amount": 4000,
                "room_type": "shared",
                "is_available": True,
                "latitude": 23.5570,
                "longitude": 87.3050,
                "distance_campus": "🚶 950m (11 min walk / 3 min cycle) to NIT Gate",
                "distance_mall": "🎬 4.0 km to Junction Mall",
                "distance_market": "🛍️ 2.4 km to Benachity",
                "distance_food": "🌯 1.1 km to Hostel Haven",
                "image_url": "/static/assets/rooms/jemua_horizon.jpg",
                "owner_id": rahul.id
            },
            {
                "title": "Muchipara Highway Studio (Near GT Road Bus Stand)",
                "description": "Independent studio room near Muchipara bus terminus. Super convenient for students who travel frequently to Kolkata or Asansol. Direct bus and auto stand right outside.",
                "city": "Durgapur",
                "locality": "Muchipara (GT Road)",
                "rent_amount": 4800,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5290,
                "longitude": 87.3320,
                "distance_campus": "🚌 3.8 km (10 min e-rickshaw) to NIT DGP",
                "distance_mall": "🎬 4.2 km to Junction Mall",
                "distance_market": "🛍️ 4.5 km to Benachity",
                "distance_food": "🍛 100m to Muchipara Dhaba & Food Stalls",
                "image_url": "/static/assets/rooms/muchipara_studio.jpg",
                "owner_id": priya.id
            },
            {
                "title": "Madhusudan Park Boys PG (Fuljhore)",
                "description": "One of the most popular student hubs in Fuljhore. Single room with attached washroom, balcony, geyser for winter sems, study table, and inverter backup.",
                "city": "Durgapur",
                "locality": "Madhusudan Park, Fuljhore",
                "rent_amount": 4600,
                "room_type": "single",
                "is_available": True,
                "latitude": 23.5535,
                "longitude": 87.2965,
                "distance_campus": "🚶 300m (4 min walk) to NIT DGP North Gate",
                "distance_mall": "🎬 3.0 km to Junction Mall",
                "distance_market": "🛍️ 1.6 km to Benachity Market",
                "distance_food": "🍲 400m to Hostel Haven Food Street",
                "image_url": "/static/assets/rooms/madhusudan_park.jpg",
                "owner_id": sourav.id
            },
            {
                "title": "City Centre Ananda Housing (Near Junction Mall)",
                "description": "High-standard shared room in 3BHK flat. Walking distance to Inox movies, food court, and City Centre bus stand. 24/7 security, high-speed WiFi, modern kitchen.",
                "city": "Durgapur",
                "locality": "City Centre (Anandamela Ground)",
                "rent_amount": 4800,
                "room_type": "shared",
                "is_available": True,
                "latitude": 23.5360,
                "longitude": 87.3010,
                "distance_campus": "🚌 1.9 km (5 min auto) to NIT DGP Main Gate",
                "distance_mall": "🎬 400m (5 min walk) to Junction Mall",
                "distance_market": "🛍️ 2.8 km to Benachity",
                "distance_food": "🍔 350m to City Centre Restaurants",
                "image_url": "/static/assets/rooms/ananda_housing.jpg",
                "owner_id": ankit.id
            },
            {
                "title": "Salt Lake Sector V Tech Studio (Kolkata)",
                "description": "Walkable to Wipro, TCS & DLF IT parks. Fully air-conditioned, high-speed internet, elevator, security surveillance, laundry facilities. Designed for tech interns.",
                "city": "Kolkata",
                "locality": "Salt Lake Sector V",
                "rent_amount": 9500,
                "room_type": "single",
                "is_available": True,
                "latitude": 22.5800,
                "longitude": 88.4350,
                "distance_campus": "🚇 200m to Sector V Metro Station",
                "distance_mall": "🏢 300m to Central Mall New Town",
                "distance_market": "🛍️ 100m to College More Grocery & Food Hub",
                "distance_food": "☕ 50m to Tech Park Food Street",
                "image_url": "/static/assets/rooms/saltlake_sector5.jpg",
                "owner_id": rahul.id
            },
            {
                "title": "New Town Action Area 1 Twin Sharing (Kolkata)",
                "description": "Opposite Candor TechSpace. Twin beds, separate study desks, shared kitchen with microwave and water purifier, twice-weekly cleaning included.",
                "city": "Kolkata",
                "locality": "New Town Action Area 1",
                "rent_amount": 6000,
                "room_type": "shared",
                "is_available": True,
                "latitude": 22.5890,
                "longitude": 88.4620,
                "distance_campus": "🚌 300m to Candor TechSpace Bus Terminal",
                "distance_mall": "🎬 800m to Axis Mall & Multiplex",
                "distance_market": "🛍️ 200m to New Town Daily Market",
                "distance_food": "🍛 150m to Food Court Street",
                "image_url": "/static/assets/rooms/newtown_action_area.jpg",
                "owner_id": priya.id
            }
        ]

        created_rooms = []
        for r in rooms_data:
            existing = db.query(models.Room).filter(
                models.Room.title == r["title"],
                models.Room.owner_id == r["owner_id"]
            ).first()
            if not existing:
                room_obj = models.Room(**r)
                db.add(room_obj)
                db.commit()
                db.refresh(room_obj)
                created_rooms.append(room_obj)
                print(f"  [OK] Created listing: {r['title']} ({r['locality']})")
            else:
                # Update with rich locality, distance and image attributes
                for key, val in r.items():
                    setattr(existing, key, val)
                db.commit()
                created_rooms.append(existing)
                print(f"  [OK] Updated listing: {r['title']} ({r['locality']})")


        # Also ensure legacy prototype listings 1-9 are updated with authentic attributes
        legacy_updates = {
            1: {'title': 'Godrej Waterside Studio Flat (Salt Lake Sector V)', 'locality': 'Salt Lake Sector V (Near College More)', 'city': 'Kolkata', 'rent_amount': 8000, 'image_url': '/static/assets/rooms/kolkata_it_studio.jpg', 'latitude': 22.5735, 'longitude': 88.4330, 'distance_campus': '🚇 150m to Sector V Metro Station', 'distance_mall': '🏢 250m to Central Mall New Town', 'distance_market': '🛍️ 100m to College More Grocery Hub', 'distance_food': '☕ 50m to Godrej Waterside Food Stalls'},
            2: {'title': 'Prantika Housing Complex 1BHK (Near NIT DGP)', 'locality': 'Prantika (NIT Main Gate)', 'city': 'Durgapur', 'rent_amount': 6000, 'image_url': '/static/assets/rooms/prantika_flat.jpg', 'latitude': 23.5480, 'longitude': 87.2940, 'distance_campus': '🚶 200m (3 min walk) to NIT DGP Main Gate', 'distance_mall': '🎬 2.9 km to Junction Mall', 'distance_market': '🛍️ 1.5 km to Benachity Market', 'distance_food': '🌯 400m to Nescafe & Hostel Haven'},
            3: {'title': 'B-Zone Steel Township Flat (Near A-Zone Market)', 'locality': 'B-Zone (Steel Township)', 'city': 'Durgapur', 'rent_amount': 3800, 'image_url': '/static/assets/rooms/bzone_green_avenue.jpg', 'latitude': 23.5430, 'longitude': 87.2870, 'distance_campus': '🚶 400m (5 min walk) to NIT West Gate & Hall 7', 'distance_mall': '🎬 2.5 km to Junction Mall', 'distance_market': '🛍️ 800m to A-Zone Market', 'distance_food': '🍲 350m to Hostel Haven'},
            4: {'title': 'Muchipara GT Road Scholar Room (GT Road)', 'locality': 'Muchipara (GT Road Junction)', 'city': 'Durgapur', 'rent_amount': 4500, 'image_url': '/static/assets/rooms/muchipara_studio.jpg', 'latitude': 23.5300, 'longitude': 87.3300, 'distance_campus': '🚌 3.5 km (Direct Toto to NIT Campus)', 'distance_mall': '🎬 4.0 km to Junction Mall', 'distance_market': '🛍️ 4.2 km to Benachity', 'distance_food': '🍛 150m to Muchipara Dhaba'},
            5: {'title': 'Suhatta Housing Master Suite (City Centre)', 'locality': 'City Centre (Near Suhatta Complex)', 'city': 'Durgapur', 'rent_amount': 7500, 'image_url': '/static/assets/rooms/fortune_park_suite.jpg', 'latitude': 23.5350, 'longitude': 87.2990, 'distance_campus': '🚌 2.0 km (5 min auto) to NIT DGP Gate', 'distance_mall': '🎬 300m (4 min walk) to Junction Mall & Inox', 'distance_market': '🛍️ 2.6 km to Benachity', 'distance_food': '🍕 200m to City Centre Food Hub'},
            6: {'title': 'DLF IT Park Tech Studio (Sector V)', 'locality': 'Sector V (Opposite DLF 1)', 'city': 'Kolkata', 'rent_amount': 9500, 'image_url': '/static/assets/rooms/saltlake_sector5.jpg', 'latitude': 22.5780, 'longitude': 88.4340, 'distance_campus': '🚇 180m to Sector V Metro Station', 'distance_mall': '🏢 350m to Central Mall', 'distance_market': '🛍️ 120m to College More Market', 'distance_food': '☕ 40m to Sector V IT Food Street'},
            7: {'title': 'Action Area 1 Modern Twin Sharing (New Town)', 'locality': 'New Town Action Area 1', 'city': 'Kolkata', 'rent_amount': 6000, 'image_url': '/static/assets/rooms/newtown_action_area.jpg', 'latitude': 22.5880, 'longitude': 88.4600, 'distance_campus': '🚌 250m to Candor TechSpace', 'distance_mall': '🎬 600m to Axis Mall & Multiplex', 'distance_market': '🛍️ 180m to Daily Vegetable Market', 'distance_food': '🍛 100m to New Town Street Food'},
            8: {'title': 'Jadavpur 8B Student Flat (South Kolkata)', 'locality': 'Jadavpur (Near 8B Bus Stand)', 'city': 'Kolkata', 'rent_amount': 8000, 'image_url': '/static/assets/rooms/jadavpur_student_flat.jpg', 'latitude': 22.4980, 'longitude': 88.3680, 'distance_campus': '🚶 250m (3 min walk) to Jadavpur University', 'distance_mall': '🎬 1.2 km to South City Mall', 'distance_market': '🛍️ 50m (Directly at 8B Market Hub)', 'distance_food': '🥘 100m to Jadavpur Coffee & Roll Stalls'},
            9: {'title': 'Ruby Hospital / EM Bypass 3BHK Flatmate (Kolkata)', 'locality': 'Kasba / EM Bypass (Near Ruby Hospital)', 'city': 'Kolkata', 'rent_amount': 5000, 'image_url': '/static/assets/rooms/ruby_em_bypass.jpg', 'latitude': 22.5130, 'longitude': 88.4020, 'distance_campus': '🚇 200m to Hemanta Mukherjee (Ruby) Metro', 'distance_mall': '🎬 600m to Acropolis Mall & Geetanjali Stadium', 'distance_market': '🛍️ 150m to Ruby Daily Grocery Market', 'distance_food': '🍜 100m to EM Bypass Dhabas & Fast Food'}
        }
        for rid, leg_data in legacy_updates.items():
            l_room = db.query(models.Room).filter(models.Room.id == rid).first()
            if l_room:
                for k, v in leg_data.items():
                    setattr(l_room, k, v)
        db.commit()

        # 3. Seed verified student reviews
        reviews_data = [
            (created_rooms[0].id, priya.id, 5, "Lived here during 3rd sem! 4 min walk to North Gate saves so much commute time. WiFi speed never drops during exams."),
            (created_rooms[0].id, ankit.id, 5, "Rahul da is very chill. Power backup really saved us during monsoon endsems load-shedding."),
            (created_rooms[1].id, demo_user.id, 5, "Right behind Hall 7! Literally 3 mins to Hostel Haven momos and rolls in the evening. Very green neighborhood."),
            (created_rooms[1].id, sourav.id, 4, "Spacious 2B residential flat. DSP municipality water is super clean. Maid comes daily."),
            (created_rooms[2].id, demo_user.id, 5, "Best 1BHK in Fuljhore. Super fast fiber net, independent balcony, and very peaceful for late-night coding."),
            (created_rooms[3].id, rahul.id, 5, "Absolute silence for GATE preparation. Attached washroom is sparkling clean and owner is very respectful."),
            (created_rooms[4].id, priya.id, 4, "Benachity market is right downstairs! Grocery shopping, xerox, fruits, and medicine are all 1 minute away."),
            (created_rooms[5].id, ankit.id, 5, "Can walk to Junction Mall Inox in 2 minutes. Best place in Durgapur if you want modern city life."),
            (created_rooms[6].id, demo_user.id, 4, "Quiet B-Zone sector. Fresh air, terrace access for morning breaks, 7 mins walk to campus."),
            (created_rooms[7].id, rahul.id, 4, "Affordable shared PG near Bhiringi. Toto auto takes 3 mins to North Gate. Low electricity tariff.")
        ]

        for room_id, user_id, rating, comment in reviews_data:
            existing_rev = db.query(models.Review).filter(
                models.Review.room_id == room_id,
                models.Review.user_id == user_id
            ).first()
            if not existing_rev:
                r_obj = models.Review(room_id=room_id, user_id=user_id, rating=rating, comment=comment)
                db.add(r_obj)
                db.commit()

        # 4. Seed bookmarks
        bookmarks_data = [
            (demo_user.id, created_rooms[0].id),
            (demo_user.id, created_rooms[1].id),
            (demo_user.id, created_rooms[5].id),
            (priya.id, created_rooms[1].id),
            (priya.id, created_rooms[4].id),
            (ankit.id, created_rooms[0].id),
            (ankit.id, created_rooms[2].id),
            (sourav.id, created_rooms[5].id),
            (rahul.id, created_rooms[3].id),
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

        print("[SUCCESS] 14 authentic listings, verified student reviews, and bookmarks are ready!")

    except Exception as e:
        print(f"[ERROR] Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
