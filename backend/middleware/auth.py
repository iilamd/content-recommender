"""
Authentication middleware
"""

from functools import wraps
from flask import request, jsonify
import jwt
from backend.config import Config


def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user_id):
            return jsonify({'user_id': current_user_id})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token tidak ditemukan'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Decode token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            current_user_id = data['user_id']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token telah expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token tidak valid'}), 401
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 401
        
        # Pass user_id to the route function
        return f(current_user_id, *args, **kwargs)
    
    return decorated