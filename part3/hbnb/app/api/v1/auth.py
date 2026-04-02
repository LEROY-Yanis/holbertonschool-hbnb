#!/usr/bin/env python3
"""Authentication API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """Login resource for user authentication."""

    @api.expect(login_model)
    @api.response(400, 'Missing email or password')
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = dict(api.payload or {})
        if 'email' not in credentials or 'password' not in credentials:
            return {'error': 'email and password are required'}, 400

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    """Protected resource for testing JWT authentication."""

    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user}'}, 200
