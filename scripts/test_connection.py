"""
Test database connection
"""

import sys
sys.path.append('..')

from backend.core.database import Database
from backend.config import Config

def test_connection():
    """Test MySQL connection"""
    print("Testing database connection...")
    print(f"Host: {Config.DB_HOST}")
    print(f"User: {Config.DB_USER}")
    print(f"Database: {Config.DB_NAME}")
    print()
    
    try:
        conn = Database.get_connection()
        print("✅ Connection successful!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"✅ Connected to database: {db_name}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Tables found: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == '__main__':
    test_connection()