"""
Database connection manager dengan connection pooling
"""

import mysql.connector
from mysql.connector import Error, pooling
import logging
from backend.config import Config

logger = logging.getLogger(__name__)


class Database:
    """
    Database class dengan static method get_connection()
    
    PATTERN PENGGUNAAN:
    ------------------
    conn = None
    cursor = None
    try:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    """
    
    _connection_pool = None
    
    @classmethod
    def _init_pool(cls):
        """Initialize connection pool (lazy initialization)"""
        if cls._connection_pool is None:
            try:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=10,
                    pool_reset_session=True,
                    host=Config.DATABASE_CONFIG['host'],
                    user=Config.DATABASE_CONFIG['user'],
                    password=Config.DATABASE_CONFIG['password'],
                    database=Config.DATABASE_CONFIG['database'],
                    autocommit=False
                )
                logger.info("✅ Database connection pool initialized")
            except Error as e:
                logger.error(f"❌ Failed to create connection pool: {e}")
                raise
    
    @staticmethod
    def get_connection():
        """
        Get MySQL connection from pool
        
        Returns:
        --------
        connection
            MySQL connection object
            
        Raises:
        -------
        Error
            If connection fails
            
        Usage:
        ------
        conn = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)
            # ... do queries
        finally:
            if conn:
                conn.close()  # Return to pool
        """
        try:
            # Initialize pool if not exists
            if Database._connection_pool is None:
                Database._init_pool()
            
            # Get connection from pool
            conn = Database._connection_pool.get_connection()
            
            # Test connection
            if not conn.is_connected():
                conn.reconnect()
            
            return conn
            
        except Error as e:
            logger.error(f"❌ Database connection error: {e}")
            raise