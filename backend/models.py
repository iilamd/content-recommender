import bcrypt
import jwt
import datetime
import logging
from backend.config import Config
from backend.core.database import Database

logger = logging.getLogger(__name__)

class User:
    def __init__(self, config):
        self.db = Database(config)
        self.db.connect()

    def create(self, username, email, password):
        try:
            # Cek user yang sudah ada
            check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
            existing_user = self.db.fetch_one(check_query, (username, email))
            
            if existing_user:
                logger.warning(f"Registration attempt with existing username/email: {username}, {email}")
                return False
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert user
            insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            result = self.db.execute(insert_query, (username, email, hashed_password))
            
            logger.info(f"User created successfully: {username}")
            return result
        except Exception as e:
            logger.error(f"User creation error: {e}")
            return False

    def authenticate(self, email, password):
        try:
            # Cari user berdasarkan email
            query = "SELECT * FROM users WHERE email = %s"
            user = self.db.fetch_one(query, (email,))
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Generate token
                token = self._generate_token(user)
                
                # Hapus password dari user data
                del user['password']
                return user, token
            
            return None, None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None, None

    def _generate_token(self, user):
        # Payload token dengan waktu kadaluarsa
        payload = {
            'user_id': user['id'],
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')