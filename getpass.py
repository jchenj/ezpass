'''
Test with:
python3 getpass.py bird
'''

import csv
import pyperclip
import argparse
import random

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DATAFILE = 'test-spreadsheet-extra-spaces.csv'
# DATAFILE = 'test-spreadsheet.csv'  # test sheet w/o extra spaces"
# Make sure that datafile is left with new line at the end so new account & password can be added correctly


def get_password_from_file(account, print_to_screen):
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
                    if print_to_screen:
                        print("Password for account '{}' is '{}'".format(account, password))
                    else:
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


def generate_random_letter(alphabet):
    index = random.randint(0, len(alphabet)-1)
    letter = alphabet[index]
    return letter


def create_password(length):
    password = ""
    for i in range(length):
        letter = generate_random_letter(ALPHABET)
        password = password + letter
    return password


def create_new_account(account, password_length):
    if check_if_account_exists(account):
        raise RuntimeError("Account '{}' already exists".format(account))
    new_pass = create_password(password_length)
    print("Creating new account with", account, new_pass)
    fields = [account, new_pass]
    with open(DATAFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('--get-pass', type=str, help='account name')
    parser.add_argument('--new-account', type=str, help='new account name')
    parser.add_argument('--print-to-screen', action='store_true', help='print password to screen', required=False,
                        default=False)
    parser.add_argument('--password-length', type=int, help='password length', required=False, default=8)
    args = parser.parse_args()

    print(args)
    try:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        if args.get_pass is not None and args.new_account is not None:
            # both are set: Error
            print("Error. Can't get password & create new account at same time")
        elif args.get_pass is not None:
            get_password_from_file(args.get_pass, args.print_to_screen)
        elif args.new_account is not None:
            create_new_account(args.new_account, args.password_length)
        elif args.get_pass is None and args.new_account is None:
            print("Error. Must give an argument.")
            parser.print_help()
    except RuntimeError as err:
        print(err)
