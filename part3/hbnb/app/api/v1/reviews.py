#!/usr/bin/env python3
"""Reviews API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Review update model (without user_id and place_id)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

# Review response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Unique identifier of the review'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})


def review_to_dict(review):
    """Convert a Review object to a dictionary."""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user_id,
        'place_id': review.place_id
    }


@api.route('/')
class ReviewList(Resource):
    """Review collection resource."""

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Missing or invalid token')
    @api.marshal_with(review_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        review_data = dict(api.payload or {})

        # Admin can create reviews on behalf of a user; regular users can only create their own.
        if not is_admin or 'user_id' not in review_data:
            review_data['user_id'] = current_user_id

        # Validate required fields
        required_fields = ['text', 'rating', 'place_id']
        for field in required_fields:
            if field not in review_data:
                return {'error': f'{field} is required'}, 400

        # Check if place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        # Non-admin users cannot review their own place.
        if not is_admin and place.owner_id == review_data['user_id']:
            return {'error': 'You cannot review your own place'}, 400

        # Non-admin users cannot review the same place twice.
        if not is_admin and facade.user_has_reviewed_place(review_data['user_id'], review_data['place_id']):
            return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return review_to_dict(new_review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        return [review_to_dict(review) for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Single review resource."""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """Get review details by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review_to_dict(review), 200

    @api.expect(review_update_model)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.marshal_with(review_response_model)
    @jwt_required()
    def put(self, review_id):
        """Update review information."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Check ownership - only the review creator or admin can modify
        if review.user_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload

        try:
            updated_review = facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return review_to_dict(updated_review), 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Check ownership - only the review creator or admin can delete
        if review.user_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        if not facade.delete_review(review_id):
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200