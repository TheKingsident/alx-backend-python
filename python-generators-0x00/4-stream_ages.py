#!/usr/bin/python3
"""Module to stream ages from a database"""

import mysql.connector
from mysql.connector import errorcode
from seed import connect_to_prodev

def stream_ages():
    stream_connection = connect_to_prodev()
    if not stream_connection:
        print("Failed to connect to the database.")
        return
    try:
        stream_cursor = stream_connection.cursor(dictionary=True)
        stream_cursor.execute("SELECT age FROM user_data")
        for row in stream_cursor:
            try:
                yield int(row["age"])
            except Exception as e:
                print("Error:", e, row)
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

def average_age():
    """Calculates the average age as the gen function streams ages"""
    total_age = 0
    count = 0
    for age in stream_ages():
        total_age += age
        count += 1
    if count == 0:
        return 0
    return f'Average age of users: {total_age / count:.2f}'