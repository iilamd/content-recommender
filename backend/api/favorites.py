"""
Favorites API routes
"""

from flask import Blueprint, request, jsonify
from backend.models import Favorite, ActivityLog
from backend.middleware import token_required
from backend.config import Config

favorites_bp = Blueprint('favorites', __name__)
favorite_model = Favorite(Config.DATABASE_CONFIG)
activity_log = ActivityLog(Config.DATABASE_CONFIG)


@favorites_bp.route('/', methods=['GET'])
@token_required
def get_favorites(current_user_id):
    """Get user's favorites"""
    favorites = favorite_model.get_by_user(current_user_id)

    return jsonify({
        'favorites': favorites,
        'count': len(favorites)
    }), 200


@favorites_bp.route('/', methods=['POST'])
@token_required
def add_favorite(current_user_id):
    """Add content to favorites"""
    data = request.get_json()
    content_id = data.get('content_id')

    if not content_id:
        return jsonify({'message': 'Content ID harus diisi'}), 400

    if favorite_model.add(current_user_id, content_id):
        activity_log.add(current_user_id, 'add_favorite')
        return jsonify({'message': 'Berhasil ditambahkan ke favorit'}), 201
    else:
        return jsonify({'message': 'Konten sudah ada di favorit'}), 400


@favorites_bp.route('/<int:favorite_id>', methods=['DELETE'])
@token_required
def delete_favorite(current_user_id, favorite_id):
    """Delete favorite"""
    if favorite_model.delete(favorite_id, current_user_id):
        activity_log.add(current_user_id, 'remove_favorite')
        return jsonify({'message': 'Berhasil dihapus dari favorit'}), 200
    else:
        return jsonify({'message': 'Favorit tidak ditemukan'}), 404