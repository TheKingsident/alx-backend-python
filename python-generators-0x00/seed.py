#!/usr/bin/python3

import mysql.connector
from mysql.connector import errorcode

def connect_db():
    """Connect to the MySQL database server"""

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("username and/or password is invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return None

def create_database(connection):
    """Create a new database"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()