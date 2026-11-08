# Authentication Flow

## Overview

This API uses **JWT (JSON Web Tokens)** with an access token + refresh token pair. All protected endpoints require a valid access token in the `Authorization` header.

## Registration Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Serializer
    participant DB as PostgreSQL

    Client->>API: POST /api/auth/register/ {email, password}
    API->>Serializer: Validate input
    Serializer->>Serializer: Check password == password_confirm
    Serializer->>DB: Check email not taken
    DB-->>Serializer: OK
    Serializer->>DB: INSERT user (password hashed via set_password)
    DB-->>API: user created
    API-->>Client: 201 Created {id, email}