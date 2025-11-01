from flask_restx import Namespace, Resource, fields
from app.services import facade

api_rvw = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api_rvw.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api_rvw.route('/')
class ReviewList(Resource):
    @api_rvw.expect(review_model)
    @api_rvw.response(201, 'Review successfully created')
    @api_rvw.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review_data = api_rvw.payload
            
            # Validate user exists
            user = facade.get_user(review_data.get('user_id'))
            if not user:
                return {'error': 'User not found'}, 400
            
            # Validate place exists
            place = facade.get_place(review_data.get('place_id'))
            if not place:
                return {'error': 'Place not found'}, 400
            
            new_review = facade.create_review(review_data)
            if not new_review:
                return {'error': 'Invalid input data'}, 400
            
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
                'created_at': new_review.created_at,
                'updated_at': new_review.updated_at
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api_rvw.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            }
            for review in reviews
        ], 200

@api_rvw.route('/<review_id>')
class ReviewResource(Resource):
    @api_rvw.response(200, 'Review details retrieved successfully')
    @api_rvw.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at,
            'updated_at': review.updated_at
        }, 200

    @api_rvw.expect(review_model)
    @api_rvw.response(200, 'Review updated successfully')
    @api_rvw.response(404, 'Review not found')
    @api_rvw.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        try:
            review_data = api_rvw.payload
            # Don't allow updating user_id or place_id
            if 'user_id' in review_data:
                del review_data['user_id']
            if 'place_id' in review_data:
                del review_data['place_id']
            
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at,
                'updated_at': updated_review.updated_at
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api_rvw.response(200, 'Review deleted successfully')
    @api_rvw.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        success = facade.delete_review(review_id)
        if success:
            return {'message': 'Review deleted successfully'}, 200
        else:
            return {'error': 'Failed to delete review'}, 400
