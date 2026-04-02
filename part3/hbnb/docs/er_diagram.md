# HBnB Entity-Relationship Diagram

This document contains the ER diagram for the HBnB database schema using Mermaid.js notation.

## Database Schema

```mermaid
erDiagram
    USERS {
        VARCHAR(36) id PK "UUID primary key"
        VARCHAR(50) first_name "Required"
        VARCHAR(50) last_name "Required"
        VARCHAR(120) email UK "Unique email"
        VARCHAR(128) password "Hashed password"
        BOOLEAN is_admin "Admin flag"
        DATETIME created_at
        DATETIME updated_at
    }

    PLACES {
        VARCHAR(36) id PK "UUID primary key"
        VARCHAR(100) title "Required"
        TEXT description
        DECIMAL price "Must be >= 0"
        DECIMAL latitude "Range: -90 to 90"
        DECIMAL longitude "Range: -180 to 180"
        VARCHAR(36) owner_id FK "References users(id)"
        DATETIME created_at
        DATETIME updated_at
    }

    REVIEWS {
        VARCHAR(36) id PK "UUID primary key"
        TEXT text "Required"
        INTEGER rating "Range: 1-5"
        VARCHAR(36) place_id FK "References places(id)"
        VARCHAR(36) user_id FK "References users(id)"
        DATETIME created_at
        DATETIME updated_at
    }

    AMENITIES {
        VARCHAR(36) id PK "UUID primary key"
        VARCHAR(50) name UK "Unique name"
        VARCHAR(255) description
        DATETIME created_at
        DATETIME updated_at
    }

    PLACE_AMENITY {
        VARCHAR(36) place_id PK,FK "References places(id)"
        VARCHAR(36) amenity_id PK,FK "References amenities(id)"
    }

    %% Relationships
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES }|--|{ AMENITIES : "has many through"
    PLACES ||--o{ PLACE_AMENITY : ""
    AMENITIES ||--o{ PLACE_AMENITY : ""
```

## Relationship Descriptions

| Relationship | Type | Description |
|--------------|------|-------------|
| `USERS → PLACES` | One-to-Many | A user can own multiple places |
| `USERS → REVIEWS` | One-to-Many | A user can write multiple reviews |
| `PLACES → REVIEWS` | One-to-Many | A place can have multiple reviews |
| `PLACES ↔ AMENITIES` | Many-to-Many | Places can have multiple amenities, amenities can belong to multiple places |

## Constraints

### Users Table
- `id`: Primary key (UUID)
- `email`: Unique constraint
- `is_admin`: Default FALSE

### Places Table
- `id`: Primary key (UUID)
- `price`: CHECK constraint (>= 0)
- `latitude`: CHECK constraint (-90 to 90)
- `longitude`: CHECK constraint (-180 to 180)
- `owner_id`: Foreign key to users(id) with CASCADE delete

### Reviews Table
- `id`: Primary key (UUID)
- `rating`: CHECK constraint (1 to 5)
- `place_id`: Foreign key to places(id) with CASCADE delete
- `user_id`: Foreign key to users(id) with CASCADE delete
- `(user_id, place_id)`: Unique constraint (one review per user per place)

### Amenities Table
- `id`: Primary key (UUID)
- `name`: Unique constraint

### Place_Amenity Table (Junction)
- `(place_id, amenity_id)`: Composite primary key
- `place_id`: Foreign key to places(id) with CASCADE delete
- `amenity_id`: Foreign key to amenities(id) with CASCADE delete
