"""
API routes package
"""
from flask import Blueprint

# Import blueprint dari masing-masing modul
from .auth import auth_bp
from .recommendation import recommend_bp
from .favorites import favorites_bp

from backend.api.recommendation import recommend_bp
from backend.api.favorites import favorites_bp

__all__ = ['auth_bp', 'recommend_bp', 'favorites_bp']