# Database Design

## ER Diagram

```mermaid
erDiagram
    USER {
        bigint id PK
        varchar email UK "login identifier"
        varchar password "hashed"
        varchar first_name
        varchar last_name
        boolean is_active
        boolean is_staff
        boolean is_superuser
        datetime date_joined
        datetime last_login
    }

    USER_GROUPS {
        bigint id PK
        bigint user_id FK
        bigint group_id FK
    }

    USER_USER_PERMISSIONS {
        bigint id PK
        bigint user_id FK
        bigint permission_id FK
    }

    GROUP {
        bigint id PK
        varchar name UK
    }

    PERMISSION {
        bigint id PK
        varchar name
        varchar codename
        bigint content_type_id FK
    }

    USER ||--o{ USER_GROUPS : "belongs to"
    GROUP ||--o{ USER_GROUPS : "has members"
    USER ||--o{ USER_USER_PERMISSIONS : "has"
    PERMISSION ||--o{ USER_USER_PERMISSIONS : "granted to"