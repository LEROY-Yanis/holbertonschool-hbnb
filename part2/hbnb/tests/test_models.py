#!/usr/bin/env python3
"""Tests for the core business logic classes."""

import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    """Test User class creation and validation."""
    print("Testing User creation...")
    
    # Test successful user creation
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    
    # Test admin user creation
    admin_user = User(first_name="Admin", last_name="User", email="admin@example.com", is_admin=True)
    assert admin_user.is_admin is True
    
    print("User creation test passed!")
    return True


def test_user_validation():
    """Test User validation."""
    print("Testing User validation...")
    
    # Test invalid first_name
    try:
        User(first_name="", last_name="Doe", email="test@example.com")
        assert False, "Should have raised ValueError for empty first_name"
    except ValueError as e:
        assert "First name" in str(e)
    
    # Test first_name too long
    try:
        User(first_name="A" * 51, last_name="Doe", email="test@example.com")
        assert False, "Should have raised ValueError for first_name too long"
    except ValueError as e:
        assert "50 characters" in str(e)
    
    # Test invalid email format
    try:
        User(first_name="John", last_name="Doe", email="invalid-email")
        assert False, "Should have raised ValueError for invalid email"
    except ValueError as e:
        assert "Invalid email" in str(e)
    
    print("User validation test passed!")
    return True


def test_user_update():
    """Test User update functionality."""
    print("Testing User update...")
    
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    original_updated_at = user.updated_at
    
    # Wait a moment to ensure timestamp changes
    import time
    time.sleep(0.01)
    
    user.update({"first_name": "Jane"})
    assert user.first_name == "Jane"
    assert user.updated_at > original_updated_at
    
    print("User update test passed!")
    return True


def test_place_creation():
    """Test Place class creation and validation."""
    print("Testing Place creation...")
    
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    assert place.title == "Cozy Apartment"
    assert place.description == "A nice place to stay"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    assert place.reviews == []
    assert place.amenities == []
    assert place.id is not None
    
    print("Place creation test passed!")
    return True


def test_place_validation():
    """Test Place validation."""
    print("Testing Place validation...")
    
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    
    # Test invalid price (negative)
    try:
        Place(title="Test", description="", price=-100, latitude=0, longitude=0, owner=owner)
        assert False, "Should have raised ValueError for negative price"
    except ValueError as e:
        assert "positive" in str(e)
    
    # Test invalid latitude
    try:
        Place(title="Test", description="", price=100, latitude=100, longitude=0, owner=owner)
        assert False, "Should have raised ValueError for invalid latitude"
    except ValueError as e:
        assert "Latitude" in str(e)
    
    # Test invalid longitude
    try:
        Place(title="Test", description="", price=100, latitude=0, longitude=200, owner=owner)
        assert False, "Should have raised ValueError for invalid longitude"
    except ValueError as e:
        assert "Longitude" in str(e)
    
    # Test invalid owner
    try:
        Place(title="Test", description="", price=100, latitude=0, longitude=0, owner="not a user")
        assert False, "Should have raised ValueError for invalid owner"
    except ValueError as e:
        assert "Owner" in str(e)
    
    print("Place validation test passed!")
    return True


def test_place_relationships():
    """Test Place class with relationships."""
    print("Testing Place relationships...")
    
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    # Test adding a review
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    
    # Test adding an amenity
    amenity = Amenity(name="Wi-Fi")
    place.add_amenity(amenity)
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wi-Fi"
    
    print("Place relationships test passed!")
    return True


def test_review_creation():
    """Test Review class creation and validation."""
    print("Testing Review creation...")
    
    owner = User(first_name="Bob", last_name="Jones", email="bob.jones@example.com")
    place = Place(
        title="Nice House",
        description="A beautiful house",
        price=150,
        latitude=40.7128,
        longitude=-74.0060,
        owner=owner
    )
    
    reviewer = User(first_name="Carol", last_name="White", email="carol.white@example.com")
    review = Review(text="Lovely place!", rating=4, place=place, user=reviewer)
    
    assert review.text == "Lovely place!"
    assert review.rating == 4
    assert review.place == place
    assert review.user == reviewer
    assert review.id is not None
    
    print("Review creation test passed!")
    return True


def test_review_validation():
    """Test Review validation."""
    print("Testing Review validation...")
    
    owner = User(first_name="Bob", last_name="Jones", email="bob.jones@example.com")
    place = Place(
        title="Nice House",
        description="A beautiful house",
        price=150,
        latitude=40.7128,
        longitude=-74.0060,
        owner=owner
    )
    
    # Test invalid rating (too low)
    try:
        Review(text="Bad place", rating=0, place=place, user=owner)
        assert False, "Should have raised ValueError for rating too low"
    except ValueError as e:
        assert "between 1 and 5" in str(e)
    
    # Test invalid rating (too high)
    try:
        Review(text="Amazing place", rating=6, place=place, user=owner)
        assert False, "Should have raised ValueError for rating too high"
    except ValueError as e:
        assert "between 1 and 5" in str(e)
    
    # Test empty text
    try:
        Review(text="", rating=3, place=place, user=owner)
        assert False, "Should have raised ValueError for empty text"
    except ValueError as e:
        assert "required" in str(e)
    
    # Test invalid place
    try:
        Review(text="Good", rating=3, place="not a place", user=owner)
        assert False, "Should have raised ValueError for invalid place"
    except ValueError as e:
        assert "Place" in str(e)
    
    # Test invalid user
    try:
        Review(text="Good", rating=3, place=place, user="not a user")
        assert False, "Should have raised ValueError for invalid user"
    except ValueError as e:
        assert "User" in str(e)
    
    print("Review validation test passed!")
    return True


def test_amenity_creation():
    """Test Amenity class creation and validation."""
    print("Testing Amenity creation...")
    
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert amenity.id is not None
    assert amenity.created_at is not None
    assert amenity.updated_at is not None
    
    print("Amenity creation test passed!")
    return True


def test_amenity_validation():
    """Test Amenity validation."""
    print("Testing Amenity validation...")
    
    # Test empty name
    try:
        Amenity(name="")
        assert False, "Should have raised ValueError for empty name"
    except ValueError as e:
        assert "required" in str(e)
    
    # Test name too long
    try:
        Amenity(name="A" * 51)
        assert False, "Should have raised ValueError for name too long"
    except ValueError as e:
        assert "50 characters" in str(e)
    
    print("Amenity validation test passed!")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running all tests for core business logic classes")
    print("=" * 50)
    
    tests = [
        test_user_creation,
        test_user_validation,
        test_user_update,
        test_place_creation,
        test_place_validation,
        test_place_relationships,
        test_review_creation,
        test_review_validation,
        test_amenity_creation,
        test_amenity_validation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAILED: {test.__name__}: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
