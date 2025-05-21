import time
import sqlite3 
import functools
import inspect


query_cache = {}

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

def cache_query(func):
    """Decorator to caches query results."""
    @functools.wraps(func)
    def wrapper_cache_query(*args, **kwargs):
        function_signature = inspect.signature(func)
        bounded_args = function_signature.bind(*args, **kwargs)
        bounded_args.apply_defaults()

        query = bounded_args.arguments.get('query')

        if query in query_cache:
            print("Using cached result")
            return query_cache[query]
        else:
            print("Executing query and caching result")
            result = func(*args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper_cache_query

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")