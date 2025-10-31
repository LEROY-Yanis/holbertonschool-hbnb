from flask_restx import Namespace, Resource, fields
from app.services import facade

api_plc = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api_plc.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api_plc.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api_plc.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api_plc.route('/')
class PlaceList(Resource):
    @api_plc.expect(place_model)
    @api_plc.response(201, 'Place successfully created')
    @api_plc.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        pass

    @api_plc.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        pass

@api_plc.route('/<place_id>')
class PlaceResource(Resource):
    @api_plc.response(200, 'Place details retrieved successfully')
    @api_plc.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        pass

    @api_plc.expect(place_model)
    @api_plc.response(200, 'Place updated successfully')
    @api_plc.response(404, 'Place not found')
    @api_plc.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        pass

@api_plc.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api_plc.response(200, 'List of reviews for the place retrieved successfully')
    @api_plc.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass
