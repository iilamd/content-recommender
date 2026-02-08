"""
Recommendation API routes
"""

from flask import Blueprint, request, jsonify
from backend.core.recommender import ContentRecommender
from backend.models import ActivityLog
from backend.middleware import token_required
from backend.config import Config

recommend_bp = Blueprint('recommendation', __name__)
recommender = ContentRecommender()
activity_log = ActivityLog(Config.DATABASE_CONFIG)


@recommend_bp.route('/', methods=['POST'])
@token_required
def get_recommendations(current_user_id):
    data = request.get_json()

    platform = data.get('platform')
    keyword = data.get('keyword')
    category = data.get('category')
    top_n = data.get('top_n', 5)  # ✅ TAMBAH INI! Default 10

    if not platform or not keyword:
        return jsonify({'message': 'Platform dan keyword harus diisi'}), 400

    activity_log.add(current_user_id, 'search', platform, keyword)

    try:
        recommendations = recommender.get_recommendations(
            platform=platform,
            keyword=keyword,
            category=category,
            top_n=top_n  # ✅ PASS KE RECOMMENDER
        )

        return jsonify({
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500