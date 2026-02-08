"""
Activity log model
"""

import logging
from backend.core.database import Database

logger = logging.getLogger(__name__)


class ActivityLog:
    def __init__(self, db_config):
        # ✅ Simpan config saja, JANGAN buat connection di sini
        self.db_config = db_config

    def add(self, user_id, action, platform=None, keyword=None):
        """Add activity log entry."""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                INSERT INTO activity_logs (user_id, action, platform, keyword)
                VALUES (%s, %s, %s, %s)
            """, (user_id, action, platform, keyword))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error adding activity log: {e}")
            if conn:
                conn.rollback()
                
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_user(self, user_id, limit=50):
        """Get activity logs for a user."""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT *
                FROM activity_logs
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, limit))
            
            return cursor.fetchall()
            
        except Exception as e:
            logger.error(f"Error getting activity logs: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def close(self):
        """Deprecated - connections now auto-close"""
        pass