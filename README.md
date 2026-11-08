
See `docs/` for the ER diagram and authentication flow diagrams.

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | ❌ | Create a new user. |
| POST | `/api/auth/login/` | ❌ | Obtain access + refresh tokens. |
| POST | `/api/auth/refresh/` | ❌ | Get a new access token (rotation enabled). |
| POST | `/api/auth/change-password/` | ✅ | Change own password. |
| POST | `/api/auth/logout/` | ✅ | Blacklist the refresh token. |
| GET | `/api/profile/` | ✅ | Read own profile. |
| PATCH | `/api/profile/` | ✅ | Update own profile (`first_name`, `last_name`). |

**Auth header format:** `Authorization: Bearer <access_token>`

## Try the API in 60 Seconds

1. Start the server: `python manage.py runserver`
2. Open **Postman** → **Import** → select `docs/postman_collection.json`
3. Run **"1. Register"** → creates a demo user
4. Run **"2. Login"** → tokens are saved automatically
5. Run any protected request (e.g. **"4. Get Profile"**) — it works without any manual token setup

The collection **auto-saves** the access and refresh tokens to collection variables after login and refresh.

## Documentation

- [Database Design & ER Diagram](docs/database.md)
- [Authentication Flow Diagrams](docs/authentication-flow.md)
- [Postman Collection](docs/postman_collection.json)

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 15+

### Steps

```bash
# 1. Clone
git clone https://github.com/Mansour13737/educational-auth-api.git
cd educational-auth-api

# 2. Create virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials and a Django secret key

# 5. Create the database
psql -U postgres -c "CREATE DATABASE auth_api_db;"
psql -U postgres -c "CREATE USER auth_api_user WITH PASSWORD 'your_password';"
psql -U postgres -c "ALTER USER auth_api_user CREATEDB;"
psql -U postgres -d auth_api_db -c "GRANT ALL ON SCHEMA public TO auth_api_user;"

# 6. Apply migrations
python manage.py migrate

# 7. Run the server
python manage.py runserver