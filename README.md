# 🏠 RentSphere — Smart Room & Flatmate Finder API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-8A2BE2.svg?style=flat)](https://alembic.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT_Bearer-orange.svg?style=flat)](https://jwt.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-grade **REST API** built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy** designed to help students and young professionals list spare rooms, find affordable housing, and discover compatible flatmates without expensive broker fees.

---

## 💡 The Real-World Problem & Impact

### ⚠️ The Problem
Every semester and hiring cycle, millions of students and young professionals relocate to new cities. Finding affordable housing and safe flatmates remains a broken experience:
* **Predatory Brokerage Fees:** Real-estate brokers often charge 1 to 2 months of rent upfront merely for passing contact numbers.
* **Fake & Duplicate Listings:** Unregulated classified ads and social media groups are plagued with duplicate postings, outdated availability, and scams.
* **Lack of Roommate Transparency:** Most platforms only show room dimensions, ignoring living habits, room types (single vs. shared), and transparent feedback.
* **Zero Landlord/Property Accountability:** Renters rarely have an authentic, community-driven rating system to review properties or living conditions before committing.

### 🛡️ How RentSphere Solves This
RentSphere is engineered as an open, secure, direct-to-owner backend system:
1. **Direct Peer-to-Peer Listings:** Owners and flatmates list rooms directly with complete price clarity, room specifications, and availability states—eliminating the middleman entirely.
2. **Enterprise-Grade Security:** User passwords are encrypted with salted **Bcrypt** hashing. Protected operations are secured via stateless **JWT Bearer Tokens** (`python-jose`), preventing identity spoofing.
3. **Smart Duplicate Prevention:** Engineered with composite primary keys (`user_id` + `room_id`) at the database layer to prevent duplicate bookmarking and data bloat.
4. **Community Reviews & Ratings:** Integrated 1-to-many review schema enabling verified renters to score and comment on properties, creating authentic accountability.
5. **High-Performance Querying:** Built for fast multi-parameter filtering (city, room type, rent limits) combined with SQL outer joins to calculate live popularity metrics in a single query.

---

## 📌 Project Status: Building in Public 🚀

- [x] **Milestone 1: Database Architecture & Relational Design**
  - Relational schema modeling with SQLAlchemy ORM
  - Database migrations configured with Alembic
  - Secure environment configuration with Pydantic BaseSettings
- [x] **Milestone 2: Authentication & Security**
  - User registration & validation with Pydantic schemas
  - Secure password salting & hashing via Bcrypt
  - Stateless JWT token issuance (`python-jose`)
  - Route protection dependency injection (`oauth2.get_current_user`)
- [x] **Milestone 3: Room CRUD & Advanced SQL Joins / Filters**
  - Room listing, creation, updates, and deletion endpoints
  - Multi-parameter search & filtering (keyword search, city, price range, room type, availability)
  - Result pagination with `limit` and `skip` query parameters
  - High-performance SQL outer join with bookmarks table to aggregate live popularity metrics
  - Row-level ownership authorization (403 Forbidden for non-owners)
- [ ] **Milestone 4: Bookmarks & Review Rating System**
- [ ] **Milestone 5: Production Polish & Documentation**

---

## 📡 Live API Endpoints (Current Implementation)

Interactive documentation is automatically generated and accessible at `/docs` (Swagger UI) and `/redoc`:

| Method | Endpoint | Description | Access Level |
|:---|:---|:---|:---:|
| `POST` | `/users/` | Register a new user profile with hashed password | Public |
| `POST` | `/login` | Authenticate with credentials and receive signed JWT Token | Public |
| `GET` | `/users/me` | Fetch authenticated user profile via Bearer token | 🔒 Protected |
| `GET` | `/users/{id}` | Lookup public user profile information by ID | Public |
| `GET` | `/rooms/` | Discover rooms with search, city/price/type filters, pagination & bookmark counts | Public |
| `POST` | `/rooms/` | Publish a new room listing (auto-linked to authenticated owner) | 🔒 Protected |
| `GET` | `/rooms/{id}` | Retrieve room details by ID with owner profile & bookmark count | Public |
| `PUT` | `/rooms/{id}` | Update room details (enforces owner-only authorization) | 🔒 Protected |
| `DELETE` | `/rooms/{id}` | Delete room listing (enforces owner-only authorization) | 🔒 Protected |
| `GET` | `/` | API healthcheck and status endpoint | Public |

### 🔍 Advanced Room Discovery & Query Capabilities

The `GET /rooms/` endpoint supports expressive multi-parameter filtering, case-insensitive keyword search, pagination, and dynamic popularity aggregation:

| Parameter | Type | Default | Description | Example |
|---|---|---|---|---|
| `search` | `string` | `""` | Case-insensitive keyword search across `title` & `description` | `?search=balcony` |
| `city` | `string` | `null` | Filter rooms by city name (case-insensitive) | `?city=Kolkata` |
| `min_rent` | `integer` | `null` | Filter rooms with rent greater than or equal to value | `?min_rent=5000` |
| `max_rent` | `integer` | `null` | Filter rooms with rent less than or equal to value | `?max_rent=15000` |
| `room_type` | `string` | `null` | Filter by accommodation type (`single` / `shared`) | `?room_type=single` |
| `is_available` | `boolean` | `null` | Filter listings by current vacancy status | `?is_available=true` |
| `limit` | `integer` | `10` | Maximum number of listings returned per page | `?limit=20` |
| `skip` | `integer` | `0` | Pagination offset (skip N listings) | `?skip=10` |

#### ⚡ High-Performance SQL Aggregation
Every room lookup performs a single-query `LEFT OUTER JOIN` against the `bookmarks` table grouped by `rooms.id`:
```sql
SELECT rooms.*, COUNT(bookmarks.room_id) AS bookmarks
FROM rooms
LEFT OUTER JOIN bookmarks ON bookmarks.room_id = rooms.id
GROUP BY rooms.id
ORDER BY rooms.created_at DESC;
```
This eliminates N+1 query overhead and provides live popularity counters directly serialized through Pydantic v2 schemas.

---

## 🗄️ Relational Data Model

RentSphere is modeled with strict multi-table relationships to ensure data integrity and query efficiency:

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
                                    │ rating (1 to 5)                       │
                                    │ comment                               │
                                    │ created_at                            │
                                    └───────────────────────────────────────┘
```

---

## 📁 Project Structure

```
RentSphere/
├── alembic/                 # Alembic migration environment
│   ├── versions/            # Version-controlled migration revisions
│   └── env.py               # Database migration runner
├── app/
│   ├── __init__.py
│   ├── config.py            # Pydantic BaseSettings (.env loader)
│   ├── database.py          # SQLAlchemy engine & session factory
│   ├── models.py            # Relational database models (User, Room, Bookmark, Review)
│   ├── oauth2.py            # JWT token creation, verification & user dependency
│   ├── schemas.py           # Pydantic input validation & response models
│   ├── utils.py             # Bcrypt password hashing & verification utilities
│   ├── main.py              # FastAPI application initialization & CORS
│   └── routers/             # Modular route controllers
│       ├── __init__.py
│       ├── auth.py          # /login authentication endpoint
│       ├── user.py          # /users/ registration & profile endpoints
│       └── room.py          # /rooms/ CRUD, search filters & SQL join aggregation
├── .env.example             # Sanitized environment template
├── .gitignore               # Strict ignore rules (keeps secrets safe)
├── alembic.ini              # Alembic migration configuration
├── LICENSE                  # MIT License
├── README.md                # Project documentation
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
Update `.env` with your local PostgreSQL credentials:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=rentsphere
DATABASE_USERNAME=postgres
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Run Database Migrations
Apply the schema directly into PostgreSQL:
```bash
alembic upgrade head
```

### 6. Launch Server
```bash
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000/docs` to test via Swagger UI.

---

## 👨‍💻 Author
**Anubhav Paul**  
- GitHub: [@anubhavpaul753-spec](https://github.com/anubhavpaul753-spec)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
