from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from functools import wraps
from config import Config
from models import User, Favorite, ActivityLog
from recommender import ContentRecommender

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

recommender = ContentRecommender()

# Middleware untuk validasi JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token tidak ditemukan'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token tidak valid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

# Route: Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'Semua field harus diisi'}), 400
    
    if User.create(username, email, password):
        return jsonify({'message': 'Registrasi berhasil'}), 201
    else:
        return jsonify({'message': 'Email atau username sudah digunakan'}), 400

# Route: Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email dan password harus diisi'}), 400
    
    user, token = User.authenticate(email, password)
    
    if user:
        # Log activity
        ActivityLog.add(user['id'], 'login')
        
        return jsonify({
            'message': 'Login berhasil',
            'token': token,
            'user': user
        }), 200
    else:
        return jsonify({'message': 'Email atau password salah'}), 401

# Route: Get Recommendations
@app.route('/api/recommend', methods=['POST'])
@token_required
def get_recommendations(current_user_id):
    data = request.get_json()
    
    platform = data.get('platform')
    keyword = data.get('keyword')
    
    if not platform or not keyword:
        return jsonify({'message': 'Platform dan keyword harus diisi'}), 400
    
    # Log activity
    ActivityLog.add(current_user_id, 'search', platform, keyword)
    
    # Dapatkan rekomendasi
    recommendations = recommender.get_recommendations(platform, keyword)
    
    return jsonify({
        'recommendations': recommendations,
        'count': len(recommendations)
    }), 200

# Route: Get Favorites
@app.route('/api/favorites', methods=['GET'])
@token_required
def get_favorites(current_user_id):
    favorites = Favorite.get_by_user(current_user_id)
    
    return jsonify({
        'favorites': favorites,
        'count': len(favorites)
    }), 200

# Route: Add to Favorites
@app.route('/api/favorites', methods=['POST'])
@token_required
def add_favorite(current_user_id):
    data = request.get_json()
    content_id = data.get('content_id')
    
    if not content_id:
        return jsonify({'message': 'Content ID harus diisi'}), 400
    
    if Favorite.add(current_user_id, content_id):
        # Log activity
        ActivityLog.add(current_user_id, 'add_favorite')
        
        return jsonify({'message': 'Berhasil ditambahkan ke favorit'}), 201
    else:
        return jsonify({'message': 'Konten sudah ada di favorit'}), 400

# Route: Delete from Favorites
@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
@token_required
def delete_favorite(current_user_id, favorite_id):
    if Favorite.delete(favorite_id, current_user_id):
        # Log activity
        ActivityLog.add(current_user_id, 'remove_favorite')
        
        return jsonify({'message': 'Berhasil dihapus dari favorit'}), 200
    else:
        return jsonify({'message': 'Favorit tidak ditemukan'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)


## 7️⃣ File: `.env`

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "content_recommender"

SECRET_KEY = "ayokskripsi"
