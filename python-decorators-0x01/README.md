## Project File Overview

- **0-log_queries.py**: Demonstrates a decorator that logs SQL queries and their execution time before running them.
- **1-with_db_connection.py**: Shows a decorator that manages opening and closing a SQLite database connection for a function.
- **2-transactional.py**: Implements a decorator to manage database transactions, committing on success and rolling back on failure.
- **3-retry_on_failure.py**: Provides a decorator to automatically retry a database operation if it fails, with configurable retries and delay.
- **4-cache_query.py**: Contains a decorator that caches the results of SQL queries to avoid redundant database access.