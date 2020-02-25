'''
Test with:
python3 getpass.py bird
'''

import csv
import pyperclip
import argparse

DATAFILE = 'test-spreadsheet-extra-spaces.csv'
# DATAFILE = 'test-spreadsheet.csv'  # test sheet w/o extra spaces"


def get_password_from_file(account):
    account_header = 'Account-name'
    password_header = 'Password'

    # TODO: add argument validation
    # TODO: If cell [row with account_name][password col] is empty, show error "no password entered for account_name"

    with open(DATAFILE, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        found = False
        for row in reader:
            for k, v in row.items():
                if k == account_header and v.strip() == account:  # Assumes headers are free of extra spaces
                    found = True
                    password = row[password_header].strip()
                    pyperclip.copy(password)
                    print("Password for account '{}' in paste buffer".format(account))
        if not found:
            raise RuntimeError("Account '{}' not in file".format(account))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('account', type=str, help='account name')
    args = parser.parse_args()
    get_password_from_file(args.account)
