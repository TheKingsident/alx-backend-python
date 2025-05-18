#!/usr/bin/python3
"""This module contains a generator function that streams user data from a MySQL database."""

import mysql.connector
from mysql.connector import errorcode
from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """Streams user data in specified batch sizes from the MySQL database."""
    stream_connection = connect_to_prodev()
    if not stream_connection:
        print("Failed to connect to the database.")
        return
    try:
        stream_cursor = stream_connection.cursor(dictionary=True)
        stream_cursor.execute("SELECT * FROM user_data")
        
        while True:
            batch = stream_cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
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

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for row in batch:
            try:
                if int(row["age"]) > 25:
                    yield row
            except Exception as e:
                print("Error:", e, row)