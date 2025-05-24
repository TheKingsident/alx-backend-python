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
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self.cursor.fetchall()
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection and handle exceptions."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return True

def example_usage():
    """ Example usage of the DatabaseConnection context manager."""
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(dict(row))

if __name__ == "__main__":
    example_usage()