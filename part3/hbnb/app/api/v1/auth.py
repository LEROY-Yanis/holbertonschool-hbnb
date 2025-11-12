from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api_auth = Namespace('auth', description='Authentication operations')

# Define the login model for input validation and documentation
login_model = api_auth.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api_auth.route('/login')
class Login(Resource):
    @api_auth.expect(login_model, validate=True)
    @api_auth.response(200, 'Login successful')
    @api_auth.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api_auth.payload
        
        # Get user by email
        user = facade.get_user_by_email(credentials['email'])
        
        # Check if user exists and password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Create JWT token with user id and is_admin claim
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )
        
        return {
            'access_token': access_token
        }, 200
