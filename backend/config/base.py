"""
Base configuration for the application
"""

import os
class Config:
    """Base configuration class"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'content_recommender')

    DATABASE_CONFIG = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME
    }

    # JWT Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # Application Configuration
    DEBUG = True
    TESTING = False
    
    # CORS Configuration
    CORS_ORIGINS = "*"
    
    # API Configuration
    API_PREFIX = '/api'
    API_VERSION = 'v1'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with secure values
    SECRET_KEY = os.getenv('SECRET_KEY')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://yourdomain.com')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DB_NAME = 'content_recommender_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}