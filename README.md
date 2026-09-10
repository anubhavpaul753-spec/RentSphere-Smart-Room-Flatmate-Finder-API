# 🏠 RentSphere — Student Room & Flatmate Finder

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00.svg?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-16_Passed-success.svg?style=flat&logo=pytest&logoColor=white)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-grade **Full-Stack Application** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0**, and a clean, responsive **Tailwind CSS interface**. Designed to help NIT Durgapur students and Kolkata tech interns discover rooms, find compatible flatmates, read senior reviews, and bypass predatory broker fees.

---

## 💬 The Story Behind RentSphere

Hey! I'm **Anubhav**, a 2nd-year B.Tech student at **NIT Durgapur**.

Every semester, hundreds of my batchmates and seniors look for off-campus housing in B-Zone, A-Zone, Muchipara, and City Centre. We either ended up paying ₹5,000–₹10,000 in upfront broker commissions just to get a landlord's phone number, or we moved into rooms with terrible power backup, bad WiFi, and surprise restrictions during exam weeks.

I built **RentSphere** to solve this real campus headache. It connects student tenants and owners directly — with verified pricing, room specs, authentic senior reviews, and instant bookmarking.

---

## 🖥️ The Web Experience (`/app`)

Instead of handing recruiters a raw API documentation link, I built a lightweight, responsive web app that serves directly from FastAPI at `/app`:

* **⚡ 1-Click Demo Account:** Click "Try Demo Account" to immediately test protected features (posting rooms, saving bookmarks, writing reviews) without filling out a signup form.
* **🔍 Instant Campus Discovery Feed:** Real-time search across listings, filter by campus area (NIT DGP B-Zone, Main Gate, Salt Lake Sector V), room type (Single Study Room vs. Shared Flat), and a live budget slider.
* **⭐ Senior Ratings & Reviews:** Click any room's star rating to view verified comments from previous student tenants, or leave your own 1–5 star rating.
* **❤️ Live Heart Bookmarking:** 1-click bookmarking that saves directly to the PostgreSQL database with composite-key duplicate protection.
* **➕ Landlord Posting Modal:** Direct listing form for students with spare rooms or local owners.

---

## 🧠 Engineering Highlights & Architectural Decisions

### 1. Eliminating the N+1 Query Bottleneck
In a naive backend implementation, fetching 20 rooms along with their bookmark counts and average ratings would trigger **41 individual database queries**. 

To keep latency under **15ms**, I wrote a single aggregated SQL query in SQLAlchemy combining `LEFT OUTER JOIN` and `GROUP BY`:

```sql
SELECT 
    rooms.*, 
    COUNT(DISTINCT bookmarks.user_id) AS bookmarks,
    COALESCE(AVG(reviews.rating), 0.0) AS avg_rating,
    COUNT(DISTINCT reviews.id) AS reviews_count
FROM rooms
LEFT OUTER JOIN bookmarks ON bookmarks.room_id = rooms.id
LEFT OUTER JOIN reviews ON reviews.room_id = rooms.id
GROUP BY rooms.id
ORDER BY rooms.created_at DESC;
```
This handles live popularity counts and review averages in **one single roundtrip** to PostgreSQL, serialized directly through Pydantic v2 schemas.

### 2. Bulletproof Database Integrity
* **Composite Primary Keys:** The `bookmarks` table uses `(user_id, room_id)` as a composite primary key. It is physically impossible for a user to bookmark the same room twice at the database layer.
* **Anti-Self-Review Guard:** The API checks listing ownership on review submissions — landlords are strictly forbidden from rating their own rooms (`400 Bad Request`).
* **Review Spam Protection:** Submitting a review for a room you already reviewed seamlessly updates your existing review instead of bloating the database with spam.

### 3. Stateless Security
* User passwords are encrypted with salted **Bcrypt** hashing.
* Protected endpoints are locked down with **stateless JWT Bearer Tokens** (`python-jose`) verified via FastAPI dependency injection (`oauth2.get_current_user`).

---

## 🛠️ Tech Stack Breakdown

| Layer | Technology | Why I Chose It |
|---|---|---|
| **Backend Framework** | **FastAPI** (Python 3) | Automatic async support, Pydantic data validation, and built-in OpenAPI schema generation. |
| **Database & ORM** | **PostgreSQL** + **SQLAlchemy 2.0** | Robust relational ACID integrity, complex outer join capabilities, and seamless migrations via **Alembic**. |
| **Authentication** | **JWT Bearer** + **Bcrypt** | Industry-standard stateless security with zero server session overhead. |
| **Frontend UI** | **HTML5 + Tailwind CSS + Vanilla JS** | Lightweight, zero build pipeline needed, no 400MB `node_modules` bloating the repo, and loads in under 50ms. |
| **Testing** | **Pytest** + **TestClient** | Automated integration tests with 100% pass rate across auth, rooms, bookmarks, and reviews. |
| **DevOps / Container** | **Docker** + **Docker Compose** | Single-command deployment (`docker compose up`) orchestrating the API and PostgreSQL container. |

---

## 📡 REST API Endpoints

Interactive Swagger UI is available at `/docs`:

| Method | Endpoint | Description | Access |
|:---|:---|:---|:---:|
| `GET` | `/app` | Interactive Web Application interface | Public |
| `POST` | `/login` | Authenticate user credentials and return signed JWT token | Public |
| `POST` | `/users/` | Register a new user profile with hashed password | Public |
| `GET` | `/users/me` | Fetch authenticated user's profile | 🔒 Protected |
| `GET` | `/rooms/` | Discover rooms with search, filters, pagination & live metrics | Public |
| `POST` | `/rooms/` | Publish a new room listing (auto-linked to current user) | 🔒 Protected |
| `GET` | `/rooms/{id}` | Get room details with owner profile, bookmarks & rating | Public |
| `PUT` | `/rooms/{id}` | Update room details (enforces owner-only authorization) | 🔒 Protected |
| `DELETE` | `/rooms/{id}` | Delete room listing (enforces owner-only authorization) | 🔒 Protected |
| `POST` | `/bookmarks/{room_id}` | Smart Toggle: save or unsave room to bookmarks | 🔒 Protected |
| `GET` | `/bookmarks/me` | Fetch all rooms saved by the authenticated user | 🔒 Protected |
| `POST` | `/reviews/{room_id}` | Submit a 1–5 star rating and comment for a room | 🔒 Protected |
| `GET` | `/reviews/{room_id}` | Get all reviews and average rating score for a room | Public |
| `DELETE` | `/reviews/{id}` | Delete a review (enforces author-only authorization) | 🔒 Protected |
| `GET` | `/` | API status and root endpoint | Public |

---

## 🧪 Automated Testing (Pytest)

RentSphere includes an integration test suite covering authentication, room operations, bookmark toggles, and rating boundary checks:

```bash
pytest -v
```

```text
============================= test session starts =============================
tests/test_auth.py::test_root_endpoint PASSED                            [  6%]
tests/test_auth.py::test_user_registration PASSED                        [ 12%]
tests/test_auth.py::test_user_login_success PASSED                       [ 18%]
tests/test_auth.py::test_user_login_wrong_password PASSED                [ 25%]
tests/test_bookmarks.py::test_bookmark_unauthorized PASSED               [ 31%]
tests/test_bookmarks.py::test_bookmark_nonexistent_room PASSED           [ 37%]
tests/test_bookmarks.py::test_bookmark_toggle_flow PASSED                [ 43%]
tests/test_bookmarks.py::test_get_my_bookmarks PASSED                    [ 50%]
tests/test_reviews.py::test_review_unauthorized PASSED                   [ 56%]
tests/test_reviews.py::test_review_rating_bounds PASSED                  [ 62%]
tests/test_reviews.py::test_review_self_room_forbidden PASSED            [ 68%]
tests/test_reviews.py::test_review_create_and_update PASSED              [ 75%]
tests/test_rooms.py::test_get_rooms_list PASSED                          [ 81%]
tests/test_rooms.py::test_get_rooms_filter_city PASSED                   [ 87%]
tests/test_rooms.py::test_create_room_unauthorized PASSED                [ 93%]
tests/test_rooms.py::test_create_and_delete_room PASSED                  [100%]
======================= 16 passed in 0.91s ========================
```

---

## ⚡ Quickstart & Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/anubhavpaul753-spec/RentSphere-Smart-Room-Flatmate-Finder-API.git
cd RentSphere-Smart-Room-Flatmate-Finder-API
```

### 2. Set up virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure `.env`
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your local PostgreSQL credentials:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=rentsphere
DATABASE_USERNAME=postgres
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

### 5. Apply Migrations & Seed Sample Campus Listings
```bash
alembic upgrade head
python seed_data.py
```

### 6. Run the Application
```bash
uvicorn app.main:app --reload
```
* 🌐 **Interactive Web App:** Open `http://localhost:8000/app`
* 📖 **Interactive Swagger UI:** Open `http://localhost:8000/docs`

---

## 🐳 Docker Deployment

To spin up the entire application along with PostgreSQL in containers:

```bash
docker compose up --build
```
This automatically runs database health checks, applies Alembic migrations, seeds campus listings, and starts the server at `http://localhost:8000/app`.

---

## 👨‍💻 Author

**Anubhav Paul**  
* 🎓 B.Tech Undergraduate (2025–2029), **National Institute of Technology (NIT) Durgapur**
* 💻 GitHub: [@anubhavpaul753-spec](https://github.com/anubhavpaul753-spec)
* 💼 LinkedIn: [Anubhav Paul](https://www.linkedin.com/in/anubhav-paul-437769391/)
* 📧 Email: anubhavpaul753@gmail.com

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
