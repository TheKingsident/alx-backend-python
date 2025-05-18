#!/usr/bin/python3
"""This module contains a generator function that streams user data from a
    MySQL database.
"""

import mysql.connector
from mysql.connector import errorcode
def stream_users():
    """Streams user data from the MySQL database."""
    try:
        password = input("Enter your MySQL password: ")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            database='ALX_prodev'
        )
        stream_cursor = connection.cursor()
        stream_cursor.execute("SELECT * FROM user_data")
        for row in stream_cursor:
            yield row
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("username and/or password is invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.close()