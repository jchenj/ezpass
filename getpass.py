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
        for row in reader:
            for k, v in row.items():
                # print(k, v)
                if k == account_header and v.strip() == account:  # Assumes headers are free of extra spaces
                    password = row[password_header].strip()
                    pyperclip.copy(password)
                    print("Password for account '{}' in paste buffer".format(account))
                    return
    raise RuntimeError("Account '{}' not in file".format(account))


def check_if_account_exists(account):
    account_header = 'Account-name'
    password_header = 'Password'

    with open(DATAFILE, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k, v in row.items():
                # print(k, v)
                if k == account_header and v.strip() == account:  # Assumes headers are free of extra spaces
                    return True
        return False


def create_new_account(account):
    if check_if_account_exists(account):
        raise RuntimeError("Account '{}' already exists".format(account))
    print("Creating new account with", account)

# generate password
# open file for writing
# add new record for file at the end of file
# close & save file



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('--get-pass', type=str, help='account name')
    parser.add_argument('--new-account', type=str, help='new account name')
    args = parser.parse_args()

    print(args)
    try:
        if args.get_pass is not None and args.new_account is not None:
            # both are set: Error
            print("Error. Can't get password & create new account at same time")
        elif args.get_pass is not None:
            get_password_from_file(args.get_pass)
        elif args.new_account is not None:
            create_new_account(args.new_account)
    except RuntimeError as err:
        print(err)
