# HBnB Application

A RESTful API application built with Flask and Flask-RESTX, following a layered architecture pattern.

## Project Structure

```
hbnb/
├── app/                    # Core application code
│   ├── __init__.py         # Flask application factory
│   ├── api/                # Presentation layer (API endpoints)
│   │   ├── __init__.py
│   │   └── v1/             # API version 1
│   │       ├── __init__.py
│   │       ├── users.py    # User endpoints
│   │       ├── places.py   # Place endpoints
│   │       ├── reviews.py  # Review endpoints
│   │       └── amenities.py # Amenity endpoints
│   ├── models/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── user.py         # User model
│   │   ├── place.py        # Place model
│   │   ├── review.py       # Review model
│   │   └── amenity.py      # Amenity model
│   ├── services/           # Service layer (Facade pattern)
│   │   ├── __init__.py     # Facade singleton instance
│   │   └── facade.py       # HBnBFacade class
│   └── persistence/        # Persistence layer
│       ├── __init__.py
│       └── repository.py   # In-memory repository implementation
├── run.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Architecture

The application follows a three-layer architecture:

- **Presentation Layer** (`api/`): Handles HTTP requests and responses via Flask-RESTX
- **Business Logic Layer** (`models/`): Contains domain models and business rules
- **Persistence Layer** (`persistence/`): Manages data storage (currently in-memory, will be replaced with database)

The **Facade Pattern** (`services/facade.py`) provides a unified interface for communication between layers.

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   cd part2/hbnb
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask development server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`. The API documentation (Swagger UI) can be accessed at `http://127.0.0.1:5000/api/v1/`.

## Configuration

Environment-specific settings are defined in `config.py`. You can set the following environment variables:

- `SECRET_KEY`: Application secret key (default: 'default_secret_key')

## Testing

### Running Unit Tests

```bash
# Run model tests
python tests/test_models.py

# Run API endpoint tests
python -m unittest tests.test_api -v
```

### Running cURL Tests

First, start the server in one terminal:
```bash
python run.py
```

Then run the cURL tests in another terminal:
```bash
bash tests/test_curl.sh
```

### Test Coverage

| Component | Tests | Status |
|-----------|-------|--------|
| User Model | 3 tests | ✅ |
| Place Model | 3 tests | ✅ |
| Review Model | 2 tests | ✅ |
| Amenity Model | 2 tests | ✅ |
| User API | 10 tests | ✅ |
| Amenity API | 8 tests | ✅ |
| Place API | 10 tests | ✅ |
| Review API | 14 tests | ✅ |

### Validation Rules

| Entity | Attribute | Validation |
|--------|-----------|------------|
| User | first_name | Required, max 50 chars |
| User | last_name | Required, max 50 chars |
| User | email | Required, valid format, unique |
| User | is_admin | Boolean |
| Place | title | Required, max 100 chars |
| Place | price | Required, positive number |
| Place | latitude | -90.0 to 90.0 |
| Place | longitude | -180.0 to 180.0 |
| Place | owner_id | Required, must exist |
| Review | text | Required |
| Review | rating | 1 to 5 |
| Review | user_id | Required, must exist |
| Review | place_id | Required, must exist |
| Amenity | name | Required, max 50 chars |

## API Endpoints

### Users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/<id>` - Get user by ID
- `PUT /api/v1/users/<id>` - Update user

### Amenities
- `POST /api/v1/amenities/` - Create amenity
- `GET /api/v1/amenities/` - List all amenities
- `GET /api/v1/amenities/<id>` - Get amenity by ID
- `PUT /api/v1/amenities/<id>` - Update amenity

### Places
- `POST /api/v1/places/` - Create place
- `GET /api/v1/places/` - List all places
- `GET /api/v1/places/<id>` - Get place by ID
- `PUT /api/v1/places/<id>` - Update place
- `GET /api/v1/places/<id>/reviews` - Get place reviews

### Reviews
- `POST /api/v1/reviews/` - Create review
- `GET /api/v1/reviews/` - List all reviews
- `GET /api/v1/reviews/<id>` - Get review by ID
- `PUT /api/v1/reviews/<id>` - Update review
- `DELETE /api/v1/reviews/<id>` - Delete review

## Future Development

- Part 3 will replace the in-memory repository with a database-backed solution using SQLAlchemy
