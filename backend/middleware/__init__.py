"""
Middleware package
"""

from backend.middleware.auth import token_required

__all__ = ['token_required']