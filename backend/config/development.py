"""
Development-specific configuration
"""

from backend.config.base import Config


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False