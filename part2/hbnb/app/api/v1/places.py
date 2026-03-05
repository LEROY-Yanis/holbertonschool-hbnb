#!/usr/bin/env python3
"""Places API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define nested models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Place response model with nested objects
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Unique identifier of the place'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities')
})


def place_to_dict(place):
    """Convert a Place object to a dictionary."""
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        },
        'amenities': [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in place.amenities
        ]
    }


@api.route('/')
class PlaceList(Resource):
    """Place collection resource."""

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """Create a new place."""
        place_data = api.payload

        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                return {'error': f'{field} is required'}, 400

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_to_dict(new_place), 201

    @api.response(200, 'List of places retrieved successfully')
    @api.marshal_list_with(place_response_model)
    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()
        return [place_to_dict(place) for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Single place resource."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """Get place details by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place_to_dict(place), 200

    @api.expect(place_model)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(place_response_model)
    def put(self, place_id):
        """Update place information."""
        place_data = api.payload

        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Don't allow changing owner
        if 'owner_id' in place_data:
            del place_data['owner_id']

        try:
            updated_place = facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_to_dict(updated_place), 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Reviews for a specific place."""

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }
            for review in reviews
        ], 200