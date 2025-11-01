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
        try:
            place_data = api_plc.payload
            
            # Validate owner exists
            owner = facade.get_user(place_data.get('owner_id'))
            if not owner:
                return {'error': 'Owner not found'}, 400
            
            # Validate amenities exist
            amenity_ids = place_data.get('amenities', [])
            for amenity_id in amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity {amenity_id} not found'}, 400
            
            new_place = facade.create_place(place_data)
            if not new_place:
                return {'error': 'Invalid input data'}, 400
            
            # Build response with owner and amenities details
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }
            
            amenities_data = []
            for amenity_id in new_place.amenities:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    amenities_data.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
            
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner': owner_data,
                'amenities': amenities_data,
                'created_at': new_place.created_at,
                'updated_at': new_place.updated_at
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api_plc.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        result = []
        
        for place in places:
            owner = facade.get_user(place.owner_id)
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None
            
            amenities_data = []
            for amenity_id in place.amenities:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    amenities_data.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
            
            result.append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner_data,
                'amenities': amenities_data,
                'created_at': place.created_at,
                'updated_at': place.updated_at
            })
        
        return result, 200

@api_plc.route('/<place_id>')
class PlaceResource(Resource):
    @api_plc.response(200, 'Place details retrieved successfully')
    @api_plc.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Get owner details
        owner = facade.get_user(place.owner_id)
        owner_data = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'email': owner.email
        } if owner else None
        
        # Get amenities details
        amenities_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities_data.append({
                    'id': amenity.id,
                    'name': amenity.name
                })
        
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenities_data,
            'created_at': place.created_at,
            'updated_at': place.updated_at
        }, 200

    @api_plc.expect(place_model)
    @api_plc.response(200, 'Place updated successfully')
    @api_plc.response(404, 'Place not found')
    @api_plc.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        try:
            place_data = api_plc.payload
            
            # Validate amenities if provided
            if 'amenities' in place_data:
                amenity_ids = place_data.get('amenities', [])
                for amenity_id in amenity_ids:
                    amenity = facade.get_amenity(amenity_id)
                    if not amenity:
                        return {'error': f'Amenity {amenity_id} not found'}, 400
            
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'error': 'Invalid input data'}, 400
            
            # Get owner details
            owner = facade.get_user(updated_place.owner_id)
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None
            
            # Get amenities details
            amenities_data = []
            for amenity_id in updated_place.amenities:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    amenities_data.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
            
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner': owner_data,
                'amenities': amenities_data,
                'created_at': updated_place.created_at,
                'updated_at': updated_place.updated_at
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

@api_plc.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api_plc.response(200, 'List of reviews for the place retrieved successfully')
    @api_plc.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        result = []
        
        for review in reviews:
            user = facade.get_user(review.user_id)
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            })
        
        return result, 200
