#!/usr/bin/env python3
"""Places API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Place update model
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
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
    @api.response(401, 'Missing or invalid token')
    @api.marshal_with(place_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        place_data = dict(api.payload or {})

        # Admin can create a place for any owner, regular users can only create for themselves.
        if not is_admin or 'owner_id' not in place_data:
            place_data['owner_id'] = current_user_id

        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude']
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

    @api.expect(place_update_model)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.marshal_with(place_response_model)
    @jwt_required()
    def put(self, place_id):
        """Update place information."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Check ownership - only owner or admin can modify
        if place.owner_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        place_data = dict(api.payload or {})

        # Don't allow changing owner
        if 'owner_id' in place_data:
            del place_data['owner_id']

        try:
            updated_place = facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_to_dict(updated_place), 200

    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place."""
        from app import db

        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        db.session.delete(place)
        db.session.commit()
        return {'message': 'Place deleted successfully'}, 200


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
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ], 200