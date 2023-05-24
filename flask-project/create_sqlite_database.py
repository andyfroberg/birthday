import sqlite3
from sqlite3 import Error
# import uuid
# The Universally Unique Identifier module will be needed to automatically generate a unique
# user_id_number for each user who registers on the 'users' table. This user_id_number can be used
# as the "event_host" on the 'events', so they can be linked.


def create_connection():
    """
    Creates a SQLite database connection to the Birthday_Reminder.db
    """
    connection = None;
    try:
        connection = sqlite3.connect('Birthday_Reminder.db')  # Establish connection with SQLite database
        print(sqlite3.version)
    except Error as e:
        print(e)
    return connection


def create_table(connection, create_table_sql):
    """
    Creates a table from the create_table_sql statement
    """
    try:
        cursor = connection.cursor()  # Create a new cursor object
        cursor.execute(create_table_sql)  # Execute a SQL command with the cursor
    except Error as e:
        print(e)


def create_user(connection, user):
    """
    Create a new user into the users table
    """
    sql = ''' INSERT INTO users(user_id,user_password)
              VALUES(?,?) '''
    cursor = connection.cursor()  # Create a new cursor object
    cursor.execute(sql, user)  # Execute a SQL command with the cursor
    return cursor.lastrowid


def create_event(connection, event):
    """
    Create a new event into the events table
    """
    sql = ''' INSERT INTO events(event_title,event_host,date_of_event)
              VALUES(?,?,?) '''
    cursor = connection.cursor()  # Create a new cursor object
    cursor.execute(sql, event)  # Execute a SQL command with the cursor
    return cursor.lastrowid


def main():
    """
    The main entry point of the script
    """

    # Define database name
    database = r"Birthday_Reminder.db"

    # Define SQL statement to create users table
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id_number integer PRIMARY KEY,
                                        user_id text NOT NULL,
                                        user_password text NOT NULL
                                    ); """

    # Define SQL statement to create events table
    sql_create_events_table = """CREATE TABLE IF NOT EXISTS events (
                                    event_title text NOT NULL,
                                    event_host integer,
                                    date_of_event text NOT NULL,
                                    FOREIGN KEY (event_host) REFERENCES users (user_id_number)
                                );"""

    # Create a connection to the SQLite database
    connection = create_connection()

    # If the connection was successfully created
    if connection is not None:
        # Create users table
        create_table(connection, sql_create_users_table)

        # Create events table
        create_table(connection, sql_create_events_table)
    else:
        print("Error! cannot create the database connection.")

    # If connection is open
    with connection:
        # Create a dummy user
        user = ('testuser', 'password')

        # Insert the user into the users table
        user_id_number = create_user(connection, user)

        # Create a dummy event
        event = ('Birthday Party', user_id_number, '2023-06-01')

        # Insert the event into the events table
        create_event(connection, event)


if __name__ == '__main__':
    main()
