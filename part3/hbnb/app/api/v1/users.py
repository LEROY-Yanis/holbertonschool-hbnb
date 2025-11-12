from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api_usr = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api_usr.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api_usr.route('/')
class UserList(Resource):
    @api_usr.expect(user_model, validate=True)
    @api_usr.response(201, 'User successfully created')
    @api_usr.response(400, 'Email already registered')
    @api_usr.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api_usr.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Hash the password before creating the user
        password = user_data.pop('password')  # Remove password from user_data
        new_user = facade.create_user(user_data)
        new_user.hash_password(password)  # Hash the password
        
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

@api_usr.route('/<user_id>')
class UserResource(Resource):
    @api_usr.response(200, 'User details retrieved successfully')
    @api_usr.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # Use to_dict() to ensure password is not included
        return user.to_dict(), 200
    
    @jwt_required()
    @api_usr.response(200, 'User updated successfully')
    @api_usr.response(404, 'User not found')
    @api_usr.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update user details (requires authentication)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Only allow users to update their own profile or admins to update any profile
        if current_user_id != user_id and not claims.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        user_data = api_usr.payload
        # Prevent updating password through this endpoint
        if 'password' in user_data:
            del user_data['password']
        
        facade.update_user(user_id, user_data)
        return user.to_dict(), 200
