#!/usr/bin/env python3
"""Amenities API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier of the amenity'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """Amenity collection resource."""

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model, code=201)
    def post(self):
        """Register a new amenity."""
        amenity_data = api.payload

        # Validate required fields
        if 'name' not in amenity_data:
            return {'error': 'name is required'}, 400

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'description': new_amenity.description
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Retrieve a list of all amenities."""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'description': amenity.description
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Single amenity resource."""

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update amenity information."""
        amenity_data = api.payload

        # Check if amenity exists
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name,
            'description': updated_amenity.description
        }, 200