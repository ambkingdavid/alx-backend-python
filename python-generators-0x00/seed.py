#!/usr/bin/python3
import mysql.connector
import csv
import uuid

# Replace with your MySQL credentials
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_HOST = "localhost"

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST
        )
        return connection
    except mysql.connector.Error:
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

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

def create_table(connection):
    """Creates a table user_data if it does not exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, file_path):
    """Inserts data from a CSV file into the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.close()
            return
        
        insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header row
            data_to_insert = []
            for row in csv_reader:
                user_id = str(uuid.uuid4())
                name, email, age = row
                data_to_insert.append((user_id, name, email, int(age)))
            
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        if cursor:
            cursor.close()

def stream_rows_generator(connection):
    """A generator that streams rows from the user_data table one by one."""
    try:
        # Use a server-side cursor to avoid loading all data into memory
        cursor = connection.cursor(buffered=False)
        query = "SELECT * FROM user_data"
        cursor.execute(query)

        # Yield each row as it's fetched
        for row in cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
