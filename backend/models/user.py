"""
User model (MySQL manual, tanpa ORM)
"""

import bcrypt
import jwt
import mysql.connector
from datetime import datetime, timedelta
from backend.config import Config
from backend.core.database import Database


class User:
    def __init__(self, db_config):
        # ✅ JANGAN simpan connection di instance!
        self.db_config = db_config

    def create(self, username, email, password):
        """Create new user"""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            conn.commit()
            return True
            
        except mysql.connector.Error as e:
            print(f"Error creating user: {e}")
            if conn:
                conn.rollback()
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def authenticate(self, email, password):
        """Authenticate user and return user data + token"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

            if not user:
                return None, None

            if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return None, None

            token = jwt.encode(
                {
                    'user_id': user['id'],
                    'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
                },
                Config.SECRET_KEY,
                algorithm=Config.JWT_ALGORITHM
            )

            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }, token
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, user_id):
        """Get user by ID"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT id, username, email FROM users WHERE id = %s",
                (user_id,)
            )
            return cursor.fetchone()
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def close(self):
        """Deprecated - connections now auto-close"""
        pass