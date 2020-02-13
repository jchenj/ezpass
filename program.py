"""
Pseudocode:
Define the function password_manager that takes one argument, account_name
    # Validate arguments
    If account_name not in Account col of spreadsheet,
        throw error with message "account_name not in spreadsheet"
    # Get password
    If cell [row with account_name][password column] is empty,
        throw error with message "no password entered for account_name"
    # Copy password
    Copy contents of cell [row with account_name][password column] to paste buffer
    Print message "Password for account_name in print_buffer"
"""
import csv
import os
import pyperclip


def password_manager(account):
    datafile = 'test-spreadsheet.csv'
    account_header = 'Account-name'
    password_header = 'Password'

    # TODO: add argument validation
    # Read in data from spreadsheet
    with open(datafile, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k, v in row.items():
                # TODO: use strip() to take away any extra spaces from keys and values
                if k == account_header and v == account:
                    pyperclip.copy(row[password_header])
                    print("Password for account '{}' in paste buffer".format(account))
                    print(row[password_header])


password_manager('dog')
