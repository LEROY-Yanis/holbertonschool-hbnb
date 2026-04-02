#!/usr/bin/env python3

from app import create_app, db
from app.services import facade


def init_db(app):
    """Initialize the database and create tables."""
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity

        db.create_all()
        print("Database tables created successfully.")


def seed_admin_user():
    """Create an initial admin user for testing."""
    admin_email = "admin@hbnb.io"
    existing_admin = facade.get_user_by_email(admin_email)
    if not existing_admin:
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'HBnB',
            'email': admin_email,
            'is_admin': True,
            'password': 'admin1234'
        }
        facade.create_user(admin_data)
        db.session.commit()
        print(f"Admin user created: {admin_email} / admin1234")
    else:
        print(f"Admin user already exists: {admin_email}")


def seed_initial_amenities():
    """Create initial amenities."""
    amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
    for amenity_name in amenities:
        existing = facade.amenity_repo.get_amenity_by_name(amenity_name)
        if not existing:
            facade.create_amenity({'name': amenity_name})
            print(f"Amenity created: {amenity_name}")


app = create_app()

if __name__ == '__main__':
    init_db(app)
    with app.app_context():
        seed_admin_user()
        seed_initial_amenities()
    app.run(debug=True)