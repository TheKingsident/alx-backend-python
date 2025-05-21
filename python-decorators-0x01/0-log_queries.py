import sqlite3
from datetime import datetime
import functools

#### decorator to log SQL queries

def log_queries(func):
    def wrapper_log_queries(*args, **kwargs):
        print(f'Executing query: {args[0]} on {datetime.now()}')
        return func(*args, **kwargs)
    return wrapper_log_queries

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results