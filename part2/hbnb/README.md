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

## Future Development

- Part 3 will replace the in-memory repository with a database-backed solution using SQLAlchemy
- API endpoints will be implemented in subsequent tasks
