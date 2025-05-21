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

def transactional(func):
    """DEcorator to manage transactions for a function."""
    @functools.wraps(func)
    def wrapper_transactional(*args, **kwargs):
        conn = args[0]
        try:
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"Transaction error: {e}")
            conn.rollback()
        return None
    return wrapper_transactional

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
