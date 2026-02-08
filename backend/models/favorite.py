"""
Favorite model
"""

import logging
from backend.core.database import Database

logger = logging.getLogger(__name__)


class Favorite:
    def __init__(self, config):
        # ✅ Simpan config saja, JANGAN buat connection di sini
        self.config = config

    def add(self, user_id, content_id):
        """Add content to favorites. Return False kalau sudah ada."""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Cek sudah ada atau belum
            cursor.execute(
                "SELECT id FROM favorites WHERE user_id = %s AND content_id = %s",
                (user_id, content_id)
            )
            existing = cursor.fetchone()

            if existing:
                return False

            # Insert
            cursor.execute(
                "INSERT INTO favorites (user_id, content_id) VALUES (%s, %s)",
                (user_id, content_id)
            )
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error adding favorite: {e}")
            if conn:
                conn.rollback()
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_user(self, user_id):
        """Get all favorites untuk satu user, lengkap dengan data content."""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT f.id, f.content_id, c.platform, c.category, c.caption,
                       c.hashtag, c.url, c.likes, c.views, c.comments,
                       c.engagement_rate, c.is_popular, f.created_at
                FROM favorites f
                JOIN contents c ON f.content_id = c.id
                WHERE f.user_id = %s
                ORDER BY f.created_at DESC
            """, (user_id,))
            
            favorites = cursor.fetchall()

            result = []
            for fav in favorites:
                result.append({
                    'id': fav['id'],
                    'content_id': fav['content_id'],
                    'content': {
                        'id': fav['content_id'],
                        'platform': fav['platform'],
                        'category': fav['category'],
                        'caption': fav['caption'],
                        'hashtags': fav['hashtag'],
                        'video_url': fav['url'],
                        'likes': fav['likes'],
                        'views': fav['views'],
                        'comments': fav['comments'],
                        'engagement_rate': fav['engagement_rate'],
                        'is_popular': fav['is_popular'],
                        'similarity_score': 1.0
                    }
                })

            return result
            
        except Exception as e:
            logger.error(f"Error getting favorites: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self, favorite_id, user_id):
        """Delete favorite. Return False kalau tidak ditemukan."""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Cek ada atau belum sebelum hapus
            cursor.execute(
                "SELECT id FROM favorites WHERE id = %s AND user_id = %s",
                (favorite_id, user_id)
            )
            existing = cursor.fetchone()

            if not existing:
                return False

            # Delete
            cursor.execute(
                "DELETE FROM favorites WHERE id = %s AND user_id = %s",
                (favorite_id, user_id)
            )
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting favorite: {e}")
            if conn:
                conn.rollback()
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def close(self):
        """Deprecated - connections now auto-close"""
        pass