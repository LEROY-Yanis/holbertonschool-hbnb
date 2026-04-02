# HBnB Application - Part 3

This version migrates persistence from in-memory storage to SQLAlchemy and adds full entity mapping, relationships, SQL scripts, and database diagram documentation.

## Completed Milestones

### Task 5 - SQLAlchemy Repository
- Implemented generic `SQLAlchemyRepository` in `app/persistence/repository.py`.
- Preserved repository interface contract (`add`, `get`, `get_all`, `update`, `delete`, `get_by_attribute`).
- Added concrete repositories for domain entities (`UserRepository`, `PlaceRepository`, `ReviewRepository`, `AmenityRepository`).
- Refactored facade to use SQLAlchemy repositories.

### Task 6 - User Entity Mapping
- Mapped `BaseModel` to SQLAlchemy (`id`, `created_at`, `updated_at`).
- Mapped `User` entity with:
   - `first_name`, `last_name`, `email`, `password`, `is_admin`
   - unique email constraint
   - password hashing via Flask-Bcrypt
- Refactored facade user operations to route through `UserRepository`.

### Task 8 - Entity Relationships
- One-to-many:
   - User -> Places
   - User -> Reviews
   - Place -> Reviews
- Many-to-many:
   - Place <-> Amenity via association table `place_amenity`
- Added review uniqueness constraint per user/place pair.

### Task 9 - SQL Scripts
- Added full schema generation script: `sql/schema.sql`
- Added initial data script: `sql/seed_data.sql`
   - inserts admin user
   - inserts initial amenities

### Task 10 - ER Diagram (Mermaid)
- Added diagram documentation in `docs/er_diagram.md`.

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   └── repository.py
│   └── services/
│       └── facade.py
├── docs/
│   └── er_diagram.md
├── sql/
│   ├── schema.sql
│   └── seed_data.sql
├── config.py
├── requirements.txt
└── run.py
```

## Installation

```bash
cd part3/hbnb
python -m venv ../../.venv
source ../../.venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Environment variables:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `FLASK_ENV` (`development`, `testing`, `production`)
- `DATABASE_URL` (used in production config)

## Running The App

```bash
python run.py
```

Swagger UI:

- `http://127.0.0.1:5000/api/v1/`

## SQL Scripts Usage

Generate schema:

```bash
sqlite3 hbnb.db < sql/schema.sql
```

Insert initial data:

```bash
sqlite3 hbnb.db < sql/seed_data.sql
```

## Integration Notes (Task 5 Focus)

To migrate a new entity from in-memory to SQLAlchemy repository:

1. Create a repository class inheriting from `SQLAlchemyRepository`.
2. Inject the new repository in `HBnBFacade.__init__`.
3. Replace direct in-memory calls with repository CRUD methods.
4. Add entity-specific query helpers in the repository (if needed).
5. Keep API/service contracts unchanged so higher layers are unaffected.

## Verification Suggestions

Run model checks:

```bash
python tests/test_models.py
```

Run API tests:

```bash
python -m unittest tests.test_api -v
```
