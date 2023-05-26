#!/usr/bin/env python3
import requests
from datetime import datetime


def get_celebrity_dob(celebrity_name):
    """
    Returns the date of birth of a given celebrity as a datetime object.

    Args:
        celebrity_name (str): Name of the celebrity.

    Returns:
        datetime: A datetime object representing the celebrity's date of birth, or None if not available.
    """
    # Define the endpoint
    api_url = "https://api.api-ninjas.com/v1/celebrity"

    # Prepare the parameters
    params = {'name': celebrity_name.lower().replace(' ', '_')}

    # Define the headers
    headers = {'X-Api-Key': '4enulfTgfsbrl/wW7JiaoQ==jLNpv26JHetz3tHp'}

    # Make the request
    response = requests.get(api_url, headers=headers, params=params)

    # If the request was successful, return the birthday, otherwise raise an error
    response.raise_for_status()

    data = response.json()

    # If the data is empty (birthday not available), return None
    if not data:
        return None

    # Parse the date string into a datetime object and return it
    dob_str = data[0]['birthday']
    dob_datetime = datetime.strptime(dob_str, "%Y-%m-%d")

    return dob_datetime


def format_dob(dob):
    """
    Formats a date of birth as a string.

    Args:
        dob (datetime): The date of birth as a datetime object.

    Returns:
        str: The date of birth formatted as a string.
    """
    day = dob.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return dob.strftime('%A, %B') + f" {day}{suffix}"


def main():
    """
    Main function that prompts the user to enter a celebrity's name, retrieves the celebrity's birthday,
    formats it and prints it. If the birthday is not available, the user is asked to enter a different name.
    """
    while True:
        # Get the celebrity's name from the user
        name = input("Enter the celebrity's name: ")

        # Get the celebrity's date of birth
        dob = get_celebrity_dob(name)

        if dob is None:
            print(f"{name}'s birthday is not available. Please try another celebrity.")
            continue

        # Format the date of birth
        dob_str = format_dob(dob)

        # Print the result
        print(f"{name}'s birthday is {dob_str}.")
        break  # Exit the loop if the birthday information is successfully retrieved


if __name__ == '__main__':
    main()
