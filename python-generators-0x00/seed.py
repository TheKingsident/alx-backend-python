#!/usr/bin/python3

import mysql.connector
from mysql.connector import errorcode
import uuid
import pandas as pd

def connect_db():
    """Connects to the MySQL database server"""
    try:
        password = input("Enter your MySQL password: ")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
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
    """Creates a new database"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the database"""
    password = input("Enter your MySQL password: ")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            database='ALX_prodev'
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

def create_table(connection):
    """Creates a new table"""
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age DECIMAL(5, 2) NOT NULL
            )
        """)
        print("Table created")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Inserts data into the table"""
    data_file = pd.read_csv(data)
    uuid_data = [
        (str(uuid.uuid4()), row['name'],
         row['email'], row['age']) for index, row in data_file.iterrows()
    ]
    insertion_cursor = connection.cursor()
    try:
        insertion_cursor.executemany("""
            INSERT INTO user_data (user_id, name, email, age)
                                     VALUES (%s, %s, %s, %s)
        """, uuid_data)
        connection.commit()
        print("Data inserted")
    except mysql.connector.Error as err:
        print(f"Failed to insert data: {err}")
    finally:
        insertion_cursor.close()