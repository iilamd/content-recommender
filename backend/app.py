"""
Main Flask application
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from backend.config import config
from backend.api import auth_bp, recommend_bp, favorites_bp
import logging
import os

# Konfigurasi logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory pattern"""
    
    # ✅ FIX: Static folder config di sini!
    app = Flask(__name__,
                static_folder='../frontend',
                static_url_path='')
    
    app.url_map.strict_slashes = False

    # Load configuration
    app.config.from_object(config[config_name])

    # =======================
    # CORS CONFIG (AMAN & SEDERHANA)
    # =======================
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # =======================
    # REGISTER BLUEPRINTS
    # =======================
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recommend_bp, url_prefix='/api/recommend')
    app.register_blueprint(favorites_bp, url_prefix='/api/favorites')

    # =======================
    # SERVE FRONTEND (ROOT)
    # =======================
    @app.route('/')
    def index():
        """Serve frontend homepage"""
        logger.info("Serving frontend index.html")
        return send_from_directory(app.static_folder, 'index.html')
    
    # =======================
    # SERVE STATIC FILES
    # =======================
    @app.route('/<path:path>')
    def serve_static(path):
        """Serve static files (CSS, JS, images)"""
        logger.info(f"Serving static file: {path}")
        return send_from_directory(app.static_folder, path)

    # =======================
    # HEALTH CHECK
    # =======================
    @app.route('/health', methods=['GET'])
    def health_check():
        logger.info("Health check accessed")
        return jsonify({
            'status': 'healthy',
            'message': 'Content Recommender API is running'
        }), 200

    # =======================
    # API ROOT INFO
    # =======================
    @app.route('/api', methods=['GET'])
    def api_root():
        """API information endpoint"""
        return jsonify({
            'message': 'Content Recommender API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'auth': '/api/auth/*',
                'recommendations': '/api/recommend/*',
                'favorites': '/api/favorites/*'
            }
        }), 200

    # =======================
    # ERROR HANDLERS
    # =======================
    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"404 Not Found: {request.url}")
        return jsonify({'message': 'Endpoint tidak ditemukan'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 Internal Server Error: {str(error)}")
        return jsonify({'message': 'Internal server error'}), 500

    return app

# ✅ Create app instance (production env)
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# =======================
# PORT CONFIGURATION
# =======================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # ✅ Disable debug di production!
    )