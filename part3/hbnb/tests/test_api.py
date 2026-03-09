#!/usr/bin/env python3
"""Tests for the API endpoints."""

import sys
import os
import json
import unittest

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app


class TestUserAPI(unittest.TestCase):
    """Test cases for User API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_user_success(self):
        """Test successful user creation."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@hbnb.io'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@hbnb.io')
        # Password should NOT be in response
        self.assertNotIn('password', data)

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_fields(self):
        """Test user creation with missing required fields."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email."""
        # Create first user
        self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'duplicate@hbnb.io'
        })
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'duplicate@hbnb.io'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_user_first_name_too_long(self):
        """Test user creation with first_name exceeding 50 characters."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'A' * 51,
            'last_name': 'Doe',
            'email': 'test@hbnb.io'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieval of all users."""
        # Create a user first
        self.client.post('/api/v1/users/', json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@hbnb.io'
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieval of a user by ID."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Get',
            'last_name': 'ById',
            'email': 'get.byid@hbnb.io'
        })
        user_id = json.loads(create_response.data)['id']

        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], 'Get')

    def test_get_user_not_found(self):
        """Test retrieval of non-existent user."""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test user update."""
        # Create a user first
        create_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Update',
            'last_name': 'Me',
            'email': 'update.me@hbnb.io'
        })
        user_id = json.loads(create_response.data)['id']

        # Update the user
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated.user@hbnb.io'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')

    def test_update_user_not_found(self):
        """Test update of non-existent user."""
        response = self.client.put('/api/v1/users/nonexistent-id', json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@hbnb.io'
        })
        self.assertEqual(response.status_code, 404)


class TestAmenityAPI(unittest.TestCase):
    """Test cases for Amenity API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_amenity_success(self):
        """Test successful amenity creation."""
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Wi-Fi',
            'description': 'High-speed wireless internet'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_create_amenity_minimal(self):
        """Test amenity creation with only required fields."""
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Pool'
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name."""
        response = self.client.post('/api/v1/amenities/', json={
            'name': ''
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_name_too_long(self):
        """Test amenity creation with name exceeding 50 characters."""
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'A' * 51
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieval of all amenities."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_amenity_by_id(self):
        """Test retrieval of an amenity by ID."""
        # Create an amenity
        create_response = self.client.post('/api/v1/amenities/', json={
            'name': 'Parking'
        })
        amenity_id = json.loads(create_response.data)['id']

        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_not_found(self):
        """Test retrieval of non-existent amenity."""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        """Test amenity update."""
        # Create an amenity
        create_response = self.client.post('/api/v1/amenities/', json={
            'name': 'Old Name'
        })
        amenity_id = json.loads(create_response.data)['id']

        # Update the amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': 'New Name',
            'description': 'Updated description'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Name')


class TestPlaceAPI(unittest.TestCase):
    """Test cases for Place API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        # Create a user for owner
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Owner',
            'last_name': 'Test',
            'email': f'owner.{id(self)}@hbnb.io'
        })
        self.owner_id = json.loads(response.data)['id']

    def test_create_place_success(self):
        """Test successful place creation."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Cozy Apartment',
            'description': 'A nice place to stay',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Cozy Apartment')
        self.assertEqual(data['price'], 100.0)

    def test_create_place_with_amenities(self):
        """Test place creation with amenities."""
        # Create amenities first
        amenity1 = self.client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
        amenity2 = self.client.post('/api/v1/amenities/', json={'name': 'Pool'})
        amenity1_id = json.loads(amenity1.data)['id']
        amenity2_id = json.loads(amenity2.data)['id']

        response = self.client.post('/api/v1/places/', json={
            'title': 'Luxury Villa',
            'description': 'Beautiful villa',
            'price': 500.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': self.owner_id,
            'amenities': [amenity1_id, amenity2_id]
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(len(data['amenities']), 2)

    def test_create_place_invalid_price(self):
        """Test place creation with invalid price (negative)."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': -100.0,
            'latitude': 0,
            'longitude': 0,
            'owner_id': self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test place creation with invalid latitude (>90)."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 100.0,
            'longitude': 0,
            'owner_id': self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test place creation with invalid longitude (>180)."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 0,
            'longitude': 200.0,
            'owner_id': self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        """Test place creation with non-existent owner."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 0,
            'longitude': 0,
            'owner_id': 'nonexistent-owner-id'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieval of all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieval of a place by ID."""
        # Create a place
        create_response = self.client.post('/api/v1/places/', json={
            'title': 'Get Test',
            'description': 'Test',
            'price': 100.0,
            'latitude': 0,
            'longitude': 0,
            'owner_id': self.owner_id
        })
        place_id = json.loads(create_response.data)['id']

        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Get Test')
        # Check owner details are included
        self.assertIn('owner', data)
        self.assertIn('id', data['owner'])

    def test_get_place_not_found(self):
        """Test retrieval of non-existent place."""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_place(self):
        """Test place update."""
        # Create a place
        create_response = self.client.post('/api/v1/places/', json={
            'title': 'Update Test',
            'description': 'Test',
            'price': 100.0,
            'latitude': 0,
            'longitude': 0,
            'owner_id': self.owner_id
        })
        place_id = json.loads(create_response.data)['id']

        # Update the place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            'title': 'Updated Title',
            'description': 'Updated description',
            'price': 150.0,
            'latitude': 10,
            'longitude': 20,
            'owner_id': self.owner_id
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['price'], 150.0)


class TestReviewAPI(unittest.TestCase):
    """Test cases for Review API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        # Create a user
        user_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Reviewer',
            'last_name': 'Test',
            'email': f'reviewer.{id(self)}@hbnb.io'
        })
        self.user_id = json.loads(user_response.data)['id']

        # Create a place
        place_response = self.client.post('/api/v1/places/', json={
            'title': 'Review Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 0,
            'longitude': 0,
            'owner_id': self.user_id
        })
        self.place_id = json.loads(place_response.data)['id']

    def test_create_review_success(self):
        """Test successful review creation."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating_low(self):
        """Test review creation with rating below 1."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Bad place',
            'rating': 0,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_high(self):
        """Test review creation with rating above 5."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Amazing place',
            'rating': 6,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        """Test review creation with empty text."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': '',
            'rating': 3,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Test review creation with non-existent user."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Test review',
            'rating': 3,
            'user_id': 'nonexistent-user-id',
            'place_id': self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test review creation with non-existent place."""
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Test review',
            'rating': 3,
            'user_id': self.user_id,
            'place_id': 'nonexistent-place-id'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieval of all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_review_by_id(self):
        """Test retrieval of a review by ID."""
        # Create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Get test review',
            'rating': 4,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        review_id = json.loads(create_response.data)['id']

        # Get the review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_not_found(self):
        """Test retrieval of non-existent review."""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        """Test review update."""
        # Create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Original review',
            'rating': 3,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        review_id = json.loads(create_response.data)['id']

        # Update the review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Updated review',
            'rating': 5
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Updated review')
        self.assertEqual(data['rating'], 5)

    def test_delete_review(self):
        """Test review deletion."""
        # Create a review
        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Delete me',
            'rating': 1,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        review_id = json.loads(create_response.data)['id']

        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

        # Verify it's deleted
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_review_not_found(self):
        """Test deletion of non-existent review."""
        response = self.client.delete('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test retrieval of reviews for a specific place."""
        # Create a review
        self.client.post('/api/v1/reviews/', json={
            'text': 'Place review',
            'rating': 4,
            'user_id': self.user_id,
            'place_id': self.place_id
        })

        # Get reviews for the place
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_reviews_by_place_not_found(self):
        """Test retrieval of reviews for non-existent place."""
        response = self.client.get('/api/v1/places/nonexistent-id/reviews')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
