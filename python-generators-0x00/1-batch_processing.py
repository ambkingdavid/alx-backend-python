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

def stream_users_in_batches(batch_size):
    """
    A generator that fetches rows from the user_data table in batches.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        # Use a non-buffered cursor for efficient memory usage
        cursor = connection.cursor(dictionary=True, buffered=False)
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)
        
        while True:
            # Fetch a batch of rows
            batch = cursor.fetchmany(size=batch_size)
            if not batch:
                break
            yield batch
    except mysql.connector.Error as err:
        print(f"Error streaming data in batches: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batch_size):
    """
    Processes each batch of users to filter those over the age of 25.
    """
    # Loop 1: Iterates through batches from the generator
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: Iterates through each user in the current batch
        for user in batch:
            if user['age'] > 25:
                # Loop 3 (implied by print): The generator for `print`
                print(user)