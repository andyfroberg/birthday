import sqlite3
from sqlite3 import Error
import uuid


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('Birthday_Reminder.db')
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
    user_id_number = int(str(uuid.uuid4().int)[-8:])
    sql = ''' INSERT INTO users(user_id_number, user_id,user_password)
              VALUES(?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, (user_id_number, *user))
    return cursor.lastrowid


def create_event(connection, event):
    sql = ''' INSERT INTO events(event_title,event_host,day_of_year)
              VALUES(?,?, CAST((julianday(?) - julianday('2023-01-01')) + 1 AS INTEGER)) '''
    cursor = connection.cursor()
    cursor.execute(sql, event)
    return cursor.lastrowid


def main():
    """
    The main function that is the entry point of the script.
    It sets up the SQLite database and creates dummy users and events for testing.
    """
    # Define database name
    database = r"Birthday_Reminder.db"

    # Define SQL statement to create 'users' table
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    user_id_number INTEGER PRIMARY KEY,
                                    user_id text NOT NULL,
                                    user_password text NOT NULL
                                ); """

    # Define SQL statement to create 'events' table
    sql_create_events_table = """CREATE TABLE IF NOT EXISTS events (
                                    event_title text NOT NULL,
                                    event_host integer,
                                    day_of_year integer NOT NULL,
                                    FOREIGN KEY (event_host) REFERENCES users (user_id_number)
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
            users = [('hong', 'qwerty'),
                     ('sheehan', 'STAXpassword1'),
                     ('tom', 'STAXpassword2'),
                     ('andy', 'STAXpassword3'),
                     ('xiying', 'STAXpassword4')
                     ]

            # Define dummy events
            events = [
                ("Hong's TCSS 506 class", '2023-05-20'),
                ("Sheehan's Game", '2023-06-15'),
                ("Tom's Anniversary", '2023-08-15'),
                ("Andy's Birthday", '2023-07-08'),
                ("Xiying's Graduation", '2023-09-24')
            ]

            # Insert users and their respective events into the tables
            for user, event in zip(users, events):
                user_id_number = create_user(connection, user)
                create_event(connection, (event[0], user_id_number, event[1]))

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
