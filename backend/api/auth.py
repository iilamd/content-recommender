from flask import Blueprint, request, jsonify
from backend.models import User
from backend.config import Config

auth_bp = Blueprint('auth', __name__)
user_model = User(Config.DATABASE_CONFIG)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Semua field harus diisi'}), 400

    if user_model.create(username, email, password):
        return jsonify({'message': 'Registrasi berhasil'}), 201
    else:
        return jsonify({'message': 'Email atau username sudah digunakan'}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email dan password harus diisi'}), 400

    user, token = user_model.authenticate(email, password)

    if user and token:
        return jsonify({
            'message': 'Login berhasil',
            'token': token,
            'user': user
        }), 200
    else:
        return jsonify({'message': 'Email atau password salah'}), 401