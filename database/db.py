import mysql.connector
from mysql.connector import Error
from config import Config

class Database:
    """Simple database connection handler"""
    
    @staticmethod
    def get_connection():
        """Get a simple database connection"""
        try:
            connection = mysql.connector.connect(**Config.DB_CONFIG)
            return connection
        except Error as e:
            print(f"Database connection error: {e}")
            raise
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False, lastrowid=False):
        """
        Execute a SQL query safely with parameters
        Returns: query result based on parameters
        """
        connection = None
        cursor = None
        
        try:
            connection = Database.get_connection()
            cursor = connection.cursor(dictionary=True)  # Return rows as dictionaries
            
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            elif lastrowid:
                result = cursor.lastrowid
            else:
                result = cursor.rowcount
            
            connection.commit()
            return result
            
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Database error: {e}")
            raise e
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def test_connection():
        """Test if we can connect to database"""
        try:
            conn = Database.get_connection()
            conn.close()
            print("✓ Database connection successful!")
            return True
        except Error as e:
            print(f"✗ Database connection failed: {e}")
            return False