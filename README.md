# Authentication & User Profile API

A REST API built with **Django** and **Django REST Framework** for user registration, JWT authentication, and profile management.

---

## Features

- **Register** with email + password (passwords hashed with PBKDF2).
- **Log in** with email and password, returns JWT access + refresh tokens.
- **Refresh** an expired access token using a valid refresh token.
- **View** and **update** own profile (protected — requires a valid token).
- **Change password** (requires the old password as proof).
- **Log out** by blacklisting the refresh token.
- **Token rotation** enabled — each refresh invalidates the previous refresh token.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | Django 5.2 LTS |
| API | Django REST Framework 3.18 |
| Auth | djangorestframework-simplejwt 5.5 |
| Database | PostgreSQL 18 |
| Testing | pytest 9.2 + pytest-django 4.14 |
| Code quality | Ruff (planned) |

## Architecture

The API is a **single Django project** with one focused app (`accounts`). No microservices, no unnecessary abstraction.
