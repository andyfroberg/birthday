#!/usr/bin/env python3
import sqlite3
from sqlite3 import Error


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('TEST_Birthday_Reminder_2.db')
        print("SQLite version: ", sqlite3.version)
    except Error as e:
        print(e)
    return connection


def create_table(connection, create_table_sql):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(connection, user):
    sql = ''' INSERT INTO users(user_name, user_email, user_password)
              VALUES(?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, user)
    return cursor.lastrowid


def create_event(connection, event):
    # Extract the year from the date
    year = event[2].split('-')[0]
    sql = ''' INSERT INTO events(event_title, user_email, date_of_event)
              VALUES(?,?,CAST((julianday(?) - julianday(? || '-01-01')) + 1 AS INTEGER)) '''
    cursor = connection.cursor()
    # Use the extracted year and the date for the SQL command
    cursor.execute(sql, (event[0], event[1], event[2], year))
    return cursor.lastrowid


def main():
    """
    The main function that is the entry point of the script.
    It sets up the SQLite database and creates dummy users and events for testing.
    """
    # Define database name
    database = r"TEST_Birthday_Reminder_2.db"

    # Define SQL statement to create 'users' table
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    user_name TEXT NOT NULL,
                                    user_email TEXT PRIMARY KEY,
                                    user_password TEXT NOT NULL
                                ); """

    # Define SQL statement to create 'events' table
    sql_create_events_table = """CREATE TABLE IF NOT EXISTS events (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    event_title TEXT NOT NULL,
                                    user_email TEXT,
                                    date_of_event INTEGER NOT NULL,
                                    FOREIGN KEY (user_email) REFERENCES users (user_email)
                                );"""

    # Create a connection to the SQLite database
    connection = create_connection()

    # If the connection was successfully created
    if connection is not None:
        # Create 'users' table
        create_table(connection, sql_create_users_table)

        # Create 'events' table
        create_table(connection, sql_create_events_table)

        # If connection is open
        with connection:
            # Create dummy users
            users = [('Hong', 'lhhung@uw.edu', 'qwerty'),
                     ('Sheehan', 'sheehan1025@gmail.com', 'STAXpassword1'),
                     ('Tom', 'tjswanson314@gmail.com', 'STAXpassword2'),
                     ('Andy', 'andy@email.com', 'STAXpassword3'),
                     ('Xiying', 'xiying@email.com', 'STAXpassword4')
                     ]

            # Define dummy events
            events = [
                ("Hong's TCSS 506 Class", 'lhhung@uw.edu', '2023-05-20'),
                ("Hong's TCSS 506 Class", 'lhhung@uw.edu', '2023-05-27'),
                ("Hong's TCSS 506 Class", 'lhhung@uw.edu', '2023-06-03'),
                ("Hong's TCSS 506 Project Due", 'lhhung@uw.edu', '2023-06-09'),
                ("Sheehan's Game", 'sheehan1025@gmail.com', '2023-06-15'),
                ("Sheehan's Project", 'sheehan1025@gmail.com', '2022-03-01'),
                ("Sheehan's Trip", 'sheehan1025@gmail.com', '2025-05-30'),
                ("Meredith's & Tom's Anniversary", 'tjswanson314@gmail.com', '2006-08-15'),
                ("Henry's Birthday", 'tjswanson314@gmail.com', '2010-10-09'),
                ("Meredith's Birthday", 'tjswanson314@gmail.com', '1978-08-31'),
                ("Tom's Birthday", 'tjswanson314@gmail.com', '1978-08-07'),
                ("Bennett's Birthday", 'tjswanson314@gmail.com', '2014-05-29'),
                ("Andy's Party", 'andy@email.com', '2023-07-08'),
                ("Andy's 1st Day on the Job", 'andy@email.com', '2024-01-01'),
                ("Andy's Other Party", 'andy@email.com', '2023-09-31'),
                ("Xiying's Graduation", 'xiying@email.com', '2023-09-24'),
                ("Candace's Graduation", 'xiying@email.com', '2023-09-24')
            ]

            # Insert users and their respective events into the tables
            for user in users:
                create_user(connection, user)

            for event in events:
                create_event(connection, event)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
