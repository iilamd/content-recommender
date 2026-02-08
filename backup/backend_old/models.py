import mysql.connector
from config import Config
import bcrypt
import jwt
from datetime import datetime, timedelta

class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

class User:
    @staticmethod
    def create(username, email, password):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def authenticate(email, password):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Generate JWT token
            token = jwt.encode({
                'user_id': user['id'],
                'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
            }, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
            
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }, token
        
        return None, None

class Content:
    @staticmethod
    def get_all_by_platform(platform):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT * FROM contents WHERE platform = %s",
            (platform,)
        )
        contents = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return contents

class Favorite:
    @staticmethod
    def add(user_id, content_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO favorites (user_id, content_id) VALUES (%s, %s)",
                (user_id, content_id)
            )
            conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_by_user(user_id):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT f.id, f.content_id, c.platform, c.title, c.theme, 
                   c.caption, c.hashtags, f.created_at
            FROM favorites f
            JOIN contents c ON f.content_id = c.id
            WHERE f.user_id = %s
            ORDER BY f.created_at DESC
        """, (user_id,))
        
        favorites = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Format response
        result = []
        for fav in favorites:
            result.append({
                'id': fav['id'],
                'content_id': fav['content_id'],
                'content': {
                    'id': fav['content_id'],
                    'platform': fav['platform'],
                    'title': fav['title'],
                    'theme': fav['theme'],
                    'caption': fav['caption'],
                    'hashtags': fav['hashtags'],
                    'similarity_score': 1.0
                }
            })
        
        return result
    
    @staticmethod
    def delete(favorite_id, user_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM favorites WHERE id = %s AND user_id = %s",
            (favorite_id, user_id)
        )
        conn.commit()
        
        deleted = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        
        return deleted

class ActivityLog:
    @staticmethod
    def add(user_id, action, platform=None, keyword=None):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO activity_logs (user_id, action, platform, keyword) VALUES (%s, %s, %s, %s)",
            (user_id, action, platform, keyword)
        )
        conn.commit()
        
        cursor.close()
        conn.close()