import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator to manage database connection for a function."""
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    return wrapper_with_db_connection

def retry_on_failure(retries=3, delay=1):
    """Decorator to retry a funtion when it fails a set number of times"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper_retry_on_failure(*args, **kwargs):
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except sqlite3.Error as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
            print("All attempts failed.")
            return None
        return wrapper_retry_on_failure
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)