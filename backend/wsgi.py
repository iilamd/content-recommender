"""
WSGI entry point for production deployment
"""

from backend.app import create_app

# Create application instance for production
app = create_app('production')

if __name__ == "__main__":
    app.run()