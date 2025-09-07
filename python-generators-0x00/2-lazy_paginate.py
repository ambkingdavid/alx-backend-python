#!/usr/bin/python3
import mysql.connector


# Replace with your MySQL credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_HOST = "localhost"

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error:
        return None
    
def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.
    """
    connection = connect_to_prodev()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Error fetching page: {err}")
        return []
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def lazy_paginate(page_size):
    """
    A generator that lazily loads pages of user data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size