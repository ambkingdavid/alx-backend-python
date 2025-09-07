#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev

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