"""
Content model
"""

from backend.core.database import Database


class Content:
    """Content model for recommendation data"""
    
    @staticmethod
    def get_all_by_platform(platform):
        """
        Get all contents by platform
        
        Parameters:
        -----------
        platform : str
            Platform name ('youtube', 'tiktok', 'instagram')
            
        Returns:
        --------
        list
            List of content dictionaries
        """
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
    
    @staticmethod
    def get_by_id(content_id):
        """
        Get content by ID
        
        Parameters:
        -----------
        content_id : int or str
            Content ID
            
        Returns:
        --------
        dict or None
            Content dictionary if found
        """
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM contents WHERE id = %s", (content_id,))
        content = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return content