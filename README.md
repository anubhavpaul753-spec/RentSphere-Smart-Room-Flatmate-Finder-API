# 🏠 RentSphere — Smart Room & Flatmate Finder API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-8A2BE2.svg?style=flat)](https://alembic.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-grade **REST API** built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy** designed to help students and young professionals list spare rooms, find affordable housing, and discover compatible flatmates.

---

## 📌 Project Status: Building in Public 🚀

- [x] **Milestone 1: Database Architecture & Relational Design**
  - Relational schema modeling with SQLAlchemy ORM
  - Database migrations configured with Alembic
  - Secure environment configuration with Pydantic BaseSettings
- [x] **Milestone 2: Authentication & Security** *(Completed)*
  - User registration & validation with Pydantic schemas
  - Secure password salting & hashing via Bcrypt
  - Stateless JWT token issuance (`python-jose`)
  - Route protection dependency injection (`oauth2.get_current_user`)
- [ ] **Milestone 3: Room CRUD & Advanced SQL Joins / Filters** *(Next)*
- [ ] **Milestone 4: Bookmarks & Review Rating System**
- [ ] **Milestone 5: Production Polish & Documentation**

---

## 🗄️ Relational Data Model

RentSphere is modeled with multi-table relationships to ensure data integrity and query efficiency:

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

### Architectural Highlights:
1. **Composite Primary Keys (`bookmarks` table):** Prevents duplicate bookmarks by pairing `user_id` + `room_id` as a composite primary key.
2. **Cascading Deletes:** Foreign keys utilize `ondelete="CASCADE"` to prevent orphaned data records.
3. **Strict Validation:** Configured with Pydantic for input validation and serialized response models.

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
│   └── routers/             # Modular API route controllers
│       └── __init__.py
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

---

## 👨‍💻 Author
**Anubhav Paul**  
- GitHub: [@anubhavpaul753-spec](https://github.com/anubhavpaul753-spec)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
