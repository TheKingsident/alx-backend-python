import sqlite3

class DatabaseConnection:
    """Context manager for managing database connections."""
    def __init__(self):
        """Initialize the database connection."""
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Open database connection and return cursor."""
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection and handle exceptions."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return True
