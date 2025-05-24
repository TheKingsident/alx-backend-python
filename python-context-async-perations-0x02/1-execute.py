import sqlite3

class  ExecuteQuery():
    """Context manager that manages both connection and query execution."""
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open database connection, execute query, and return results."""
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            print(f"An error occurred: {exc_value}")
        return True


def example_usage():
    """Example usage of the ExecuteQuery context manager."""
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
        for row in results:
            print(dict(row))

if __name__ == "__main__":
    example_usage()
