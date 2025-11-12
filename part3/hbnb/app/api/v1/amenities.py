from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api_amnt = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api_amnt.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api_amnt.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api_amnt.expect(amenity_model)
    @api_amnt.response(201, 'Amenity successfully created')
    @api_amnt.response(400, 'Invalid input data')
    @api_amnt.response(403, 'Admin privileges required')
    def post(self):
        """Register a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        try:
            amenity_data = api_amnt.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at,
                'updated_at': new_amenity.updated_at
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api_amnt.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at,
                'updated_at': amenity.updated_at
            }
            for amenity in amenities
        ], 200

@api_amnt.route('/<amenity_id>')
class AmenityResource(Resource):
    @api_amnt.response(200, 'Amenity details retrieved successfully')
    @api_amnt.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at,
            'updated_at': amenity.updated_at
        }, 200

    @jwt_required()
    @api_amnt.expect(amenity_model)
    @api_amnt.response(200, 'Amenity updated successfully')
    @api_amnt.response(404, 'Amenity not found')
    @api_amnt.response(400, 'Invalid input data')
    @api_amnt.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        """Update an amenity's information (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        try:
            amenity_data = api_amnt.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at,
                'updated_at': updated_amenity.updated_at
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400
