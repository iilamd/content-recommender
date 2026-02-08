"""
Production-specific configuration
"""

import os
from backend.config.base import Config


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Force HTTPS
    PREFERRED_URL_SCHEME = 'https'
    
    # Secure secret key from environment
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production!")
    
    # Database connection pool
    DB_POOL_SIZE = 10
    DB_POOL_RECYCLE = 3600