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

def stream_user_ages():
    """
    A generator that yields user ages one by one from the database.
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    try:
        # Use a non-buffered cursor to avoid loading all data
        cursor = connection.cursor(buffered=False)
        query = "SELECT age FROM user_data"
        cursor.execute(query)
        
        for (age,) in cursor:
            yield age
    except mysql.connector.Error as err:
        print(f"Error streaming ages: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the generator.
    """
    total_age = 0
    count = 0
    
    # Loop 1: Consumes the generator to get each age
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found to calculate the average age.")

if __name__ == "__main__":
    calculate_average_age()