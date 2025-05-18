#!/usr/bin/python3
"""This module contains a generator function that streams user data from a MySQL database."""

from seed import connect_to_prodev
from mysql.connector import errorcode
import mysql.connector

def paginate_users(page_size, offset):
    """Paginates user data from the MySQL database."""
    stream_connection = connect_to_prodev()
    if not stream_connection:
        print("Failed to connect to the database.")
        return
    try:
        stream_cursor = stream_connection.cursor(dictionary=True)
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        stream_cursor.execute(query)
        return stream_cursor.fetchall()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("username and/or password is invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        if stream_connection:
            stream_cursor.close()
            stream_connection.close()

def lazy_paginate(page_size):
    """Lazy pagination of user data."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size