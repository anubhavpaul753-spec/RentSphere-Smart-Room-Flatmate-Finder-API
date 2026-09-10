# 🏠 RentSphere — Smart Room & Flatmate Finder (Full-Stack)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-8A2BE2.svg?style=flat)](https://alembic.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT_Bearer-orange.svg?style=flat)](https://jwt.io/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v3.0+-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Pytest](https://img.shields.io/badge/Pytest-16_Passed-success.svg?style=flat&logo=pytest&logoColor=white)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-grade **Full-Stack Application** engineered with **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM (2.0)**, and a modern **Tailwind CSS Interactive Single Page Application**. Designed to help NIT Durgapur and Kolkata students and young professionals list rooms, discover verified flatmates, bookmark favorite places, and review accommodations with zero broker fees.

---

## 🖥️ Live Interactive Web Frontend (`/app`)

RentSphere includes an interactive Single Page Application mounted directly at `/app` (or deployable independently to Vercel).

* ⚡ **1-Click Demo Mode:** Instant guest authentication without manual sign-up.
* 🔍 **Real-Time Discovery Feed:** Search listings by title, keywords, city (`Durgapur` / `Kolkata`), accommodation type (`single` / `shared`), and an interactive max rent price slider.
* ⭐ **Student Reviews & 5-Star Ratings:** Interactive star rating selector, verified student feedback modal, and real-time average calculation.
* ❤️ **Instant Bookmarking:** 1-click heart toggle synced live to PostgreSQL with smart duplicate prevention.
* ➕ **Publish Room Modal:** Clean, validated listing submission form for student landlords.

---

## 💡 The Real-World Problem & Impact

### ⚠️ The Problem
Every semester and hiring cycle, students and tech professionals relocate to academic hubs like **NIT Durgapur** and tech centers like **Kolkata (Salt Lake Sector V)**. Finding affordable housing remains broken:
* **Predatory Brokerage Fees:** Local real-estate brokers demand 1 to 2 months of rent upfront merely for passing contact phone numbers.
* **Fake & Duplicate Listings:** Unregulated classifieds are flooded with phantom listings and duplicate posts.
* **Zero Accountability & Feedback:** Renters have no authentic, community-driven rating system to review living conditions, WiFi stability, or landlord reliability before signing a lease.

### 🛡️ How RentSphere Solves This
1. **Direct Peer-to-Peer Marketplace:** Connects student landlords and prospective flatmates directly with complete pricing transparency and zero broker commissions.
2. **Enterprise-Grade Security:** Salted **Bcrypt** password hashing with stateless **JWT Bearer tokens** (`python-jose`).
3. **Smart Duplicate Prevention:** Composite primary key architecture (`user_id` + `room_id`) preventing database bloat and bookmark spam.
4. **Community Reviews & Ratings:** Verified renters score rooms 1–5 stars and leave authentic feedback. Landlords are blocked from self-reviewing (`400 Bad Request`).
5. **High-Performance SQL Aggregations:** Evaluates live bookmark counts and average ratings in a single query via `LEFT OUTER JOIN` and `GROUP BY`, eliminating N+1 query bottlenecks.

---

## 📌 Project Milestones: 100% Completed 🚀

- [x] **Milestone 1: Database Architecture & Relational Design**
  - Relational schema modeling with SQLAlchemy ORM (Users, Rooms, Bookmarks, Reviews)
  - Version-controlled migrations configured with Alembic
  - Type-safe environment configuration with Pydantic BaseSettings
- [x] **Milestone 2: Authentication & Security**
  - User registration & validation with Pydantic schemas
  - Secure password salting & hashing via Bcrypt
  - Stateless JWT token issuance and route protection dependency injection
- [x] **Milestone 3: Room CRUD & Advanced SQL Joins / Filters**
  - Multi-parameter search & filtering (keyword, city, price range, room type, availability)
  - Result pagination with `limit` and `skip` query parameters
  - Row-level ownership authorization (`403 Forbidden` for non-owners)
- [x] **Milestone 4: Bookmarks & Review Rating System**
  - Smart toggle bookmark endpoint (`POST /bookmarks/{room_id}`) with composite key uniqueness
  - Authenticated user's saved listings retrieval (`GET /bookmarks/me`)
  - 1-to-5 star review system with landlord self-review restriction and spam protection
  - Unified SQL aggregation query returning room details, bookmark counts, and average star ratings in 1 roundtrip
- [x] **Milestone 5: Production Polish, Frontend UI & Automated Testing**
  - Interactive Tailwind CSS Single Page Application served at `/app`
  - Realistic NIT Durgapur and Kolkata student campus dataset seeding script (`seed_data.py`)
  - Automated integration test suite (`pytest`) with 16 test cases passing at 100%
  - Production `Dockerfile`, `docker-compose.yml`, and `render.yaml` cloud deployment config

---

## 📡 Complete REST API Endpoints

Interactive documentation is automatically generated and accessible at `/docs` (Swagger UI) and `/redoc`:

| Method | Endpoint | Description | Access Level |
|:---|:---|:---|:---:|
| `GET` | `/app` | **Interactive Web Frontend Single Page Application** | Public |
| `POST` | `/users/` | Register a new user profile with hashed password | Public |
| `POST` | `/login` | Authenticate with credentials and receive signed JWT Token | Public |
| `GET` | `/users/me` | Fetch authenticated user profile via Bearer token | 🔒 Protected |
| `GET` | `/users/{id}` | Lookup public user profile information by ID | Public |
| `GET` | `/rooms/` | Discover rooms with search, city/price/type filters, pagination & bookmark/rating counts | Public |
| `POST` | `/rooms/` | Publish a new room listing (auto-linked to authenticated owner) | 🔒 Protected |
| `GET` | `/rooms/{id}` | Retrieve room details by ID with owner profile, bookmarks & rating | Public |
| `PUT` | `/rooms/{id}` | Update room details (enforces owner-only authorization) | 🔒 Protected |
| `DELETE` | `/rooms/{id}` | Delete room listing (enforces owner-only authorization) | 🔒 Protected |
| `POST` | `/bookmarks/{room_id}` | Smart Toggle bookmark (adds or removes bookmark) | 🔒 Protected |
| `GET` | `/bookmarks/me` | Retrieve all rooms saved/bookmarked by current user | 🔒 Protected |
| `GET` | `/bookmarks/check/{room_id}` | Fast boolean check if current user has saved room | 🔒 Protected |
| `POST` | `/reviews/{room_id}` | Submit rating (1-5 stars) and comment for a room | 🔒 Protected |
| `GET` | `/reviews/{room_id}` | Fetch all reviews and rating summary for a room | Public |
| `PUT` | `/reviews/{id}` | Update existing review (enforces author-only authorization) | 🔒 Protected |
| `DELETE` | `/reviews/{id}` | Delete a review (enforces author-only authorization) | 🔒 Protected |
| `GET` | `/` | API status and root endpoint | Public |

---

## ⚡ High-Performance SQL Aggregation

Every room listing query performs a single-query `LEFT OUTER JOIN` against both the `bookmarks` and `reviews` tables grouped by `rooms.id`:

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

This eliminates N+1 query bottlenecks and returns dynamic popularity metrics and review scores serialized directly through Pydantic v2 schemas in **< 15ms**.

---

## 🗄️ Relational Data Model

```
┌────────────────────────┐         ┌───────────────────────────────────────┐
│        users           │         │                rooms                  │
├────────────────────────┤         ├───────────────────────────────────────┤
│ id (PK)                │◄───┐     │ id (PK)                               │
│ email (Unique)         │    │     │ title                                 │
│ password (Hashed)      │    │     │ description                           │
│ phone_number           │    ├─────│ owner_id (FK -> users.id)             │
│ city                   │    │     │ city                                  │
│ created_at             │    │     │ rent_amount                           │
└────────────────────────┘    │     │ room_type ('single' / 'shared')       │
                              │     │ is_available (Boolean)                │
                              │     │ created_at                            │
                              │     └───────────────────────────────────────┘
                              │
                              │     ┌───────────────────────────────────────┐
                              │     │              bookmarks                │
                              │     ├───────────────────────────────────────┤
                              ├─────│ user_id (Composite PK, FK -> users.id)│
                              │     │ room_id (Composite PK, FK -> rooms.id)│
                              │     └───────────────────────────────────────┘
                              │
                              │     ┌───────────────────────────────────────┐
                              │     │               reviews                 │
                              │     ├───────────────────────────────────────┤
                              │     │ id (PK)                               │
                              └─────│ user_id (FK -> users.id)              │
                                    │ room_id (FK -> rooms.id)              │
                                    │ rating (1 to 5 stars)                 │
                                    │ comment                               │
                                    │ created_at                            │
                                    └───────────────────────────────────────┘
```

---

## 📁 Project Architecture

```
RentSphere/
├── alembic/                 # Alembic migration environment
│   ├── versions/            # Database schema migration revisions
│   └── env.py               # Database migration runner
├── app/
│   ├── __init__.py
│   ├── config.py            # Pydantic BaseSettings (.env loader)
│   ├── database.py          # SQLAlchemy engine & session factory
│   ├── models.py            # Relational models (User, Room, Bookmark, Review)
│   ├── oauth2.py            # JWT token creation, verification & dependency
│   ├── schemas.py           # Pydantic v2 input validation & response models
│   ├── utils.py             # Salted Bcrypt password hashing
│   ├── main.py              # FastAPI initialization, CORS & static files mount
│   └── routers/             # Modular route controllers
│       ├── __init__.py
│       ├── auth.py          # /login authentication
│       ├── user.py          # /users/ registration & profile
│       ├── room.py          # /rooms/ CRUD & multi-table SQL join aggregation
│       ├── bookmark.py      # /bookmarks/ smart toggle & saved listings
│       └── review.py        # /reviews/ 1-5 star ratings & comments
├── frontend/                # Interactive Single Page Application
│   ├── index.html           # Tailwind CSS responsive frontend
│   └── vercel.json          # Vercel cloud deployment config
├── tests/                   # Automated Integration Test Suite (Pytest)
│   ├── conftest.py          # Test client & authentication fixtures
│   ├── test_auth.py         # Registration & JWT login tests
│   ├── test_rooms.py        # Room CRUD, search & ownership tests
│   ├── test_bookmarks.py    # Bookmark toggle & my saved rooms tests
│   └── test_reviews.py      # Review constraints (1-5 range & anti-self-review)
├── seed_data.py             # Realistic campus & city dataset seeder
├── pytest.ini               # Pytest configuration
├── Dockerfile               # Production multi-stage Docker build
├── docker-compose.yml       # 1-Command containerized stack (FastAPI + Postgres)
├── render.yaml              # Render cloud deployment template
├── .env.example             # Sanitized environment template
├── .gitignore               # Strict git exclusion rules
├── LICENSE                  # MIT License
├── README.md                # Comprehensive documentation
└── requirements.txt         # Pinned project dependencies
```

---

## ⚙️ Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/anubhavpaul753-spec/RentSphere-Smart-Room-Flatmate-Finder-API.git
cd RentSphere-Smart-Room-Flatmate-Finder-API
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # On Windows
# source venv/bin/activate   # On macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Update `.env` with your PostgreSQL credentials:
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

### 5. Run Database Migrations & Seed Data
```bash
alembic upgrade head
python seed_data.py
```

### 6. Run Automated Test Suite
```bash
pytest -v
```
*(All 16 integration tests pass in ~1.3s)*

### 7. Launch Full-Stack Application
```bash
uvicorn app.main:app --reload
```
* 🌐 **Interactive Web App:** Open `http://localhost:8000/app`
* 📖 **Interactive Swagger UI:** Open `http://localhost:8000/docs`

---

## 🐳 Docker 1-Command Startup

To run the entire application (FastAPI + PostgreSQL DB) inside containers:

```bash
docker compose up --build
```
This automatically handles database health checks, applies Alembic migrations, seeds realistic data, and launches the server at `http://localhost:8000/app`.

---

## 👨‍💻 Author

**Anubhav Paul**  
* 🎓 National Institute of Technology (NIT) Durgapur
* 💻 GitHub: [@anubhavpaul753-spec](https://github.com/anubhavpaul753-spec)
* 💼 LinkedIn: [Anubhav Paul](https://www.linkedin.com/in/anubhav-paul-437769391/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
