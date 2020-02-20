'''
Test with:
python3 getpass.py bird
'''

import csv
import os
import pyperclip
import argparse


def get_password_from_file(account):
    # datafile = 'test-spreadsheet.csv'
    datafile = 'test-spreadsheet-extra-spaces.csv'
    account_header = 'Account-name'
    password_header = 'Password'

    # TODO: add argument validation
    # TODO: If account_name not in acct col of spreadsheet, throw error with message "account_name not in spreadsheet"
    # TODO: If cell [row with account_name][password col] is empty, show error "no password entered for account_name"

    with open(datafile, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k, v in row.items():
                if k == account_header and v.strip() == account:  # Assumes headers are free of extra spaces
                    password = row[password_header].strip()
                    pyperclip.copy(password)
                    print("Password for account '{}' in paste buffer".format(account))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('account', type=str, help='account name')
    args = parser.parse_args()
    get_password_from_file(args.account)
