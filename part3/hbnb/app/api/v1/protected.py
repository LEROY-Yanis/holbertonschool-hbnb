from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def admin_required():
    """Decorator to protect endpoints that require admin privileges"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('is_admin') != True:
                return jsonify({'error': 'Admin privileges required'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def jwt_required_wrapper():
    """Decorator to protect endpoints that require authentication"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        return decorator
    return wrapper
