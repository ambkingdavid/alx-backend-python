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

def stream_users():
    """
    A generator that streams rows from the user_data table one by one.
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    try:
        # Use a server-side cursor to avoid loading all data at once
        cursor = connection.cursor(dictionary=True, buffered=False)
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)

        # Iterate over the cursor, yielding each row
        for row in cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()