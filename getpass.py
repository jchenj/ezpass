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


def get_password_from_file(fname, account, print_to_screen):
    """
    Given valid account name in file, puts password for account in paste buffer.
    If optional '--print_to_screen' parameter entered, then password printed to screen instead of put in paste buffer.
    :param fname: name of file containing accounts & passwords
    :param account: account name
    :param print_to_screen: optional parameter to print password to screen
    :return: password in paste buffer (default) or printed to screen (if optional parameter used)
    """
    account_header = 'Account-name'
    password_header = 'Password'

    # TODO: add argument validation
    # TODO: If cell [row with account_name][password col] is empty, show error "no password entered for account_name"

    with open(fname, encoding='utf-8-sig') as csvfile:
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


def check_if_account_exists(fname, account):
    """
    If account exists in file, returns True. If account doesn't exist in file, returns False.
    :param account: account name
    :return: True if account in file
    """
    account_header = 'Account-name'
    password_header = 'Password'

    with open(fname, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k, v in row.items():
                # print(k, v)
                if k == account_header and v.strip() == account:  # Assumes headers are free of extra spaces
                    return True
        return False


def generate_random_letter(alphabet):
    """
    Generates random letter from alphabet
    :param alphabet: string representing full alphabet
    :return: one random letter from the alphabet
    """
    index = random.randint(0, len(alphabet)-1)
    letter = alphabet[index]
    return letter


def create_password(length):
    password = ""
    for i in range(length):
        letter = generate_random_letter(ALPHABET)
        password = password + letter
    return password


def create_new_account(fname, account, password_length):
    if check_if_account_exists(fname, account):
        raise RuntimeError("Account '{}' already exists".format(account))
    new_pass = create_password(password_length)
    print("Creating new account with", account, new_pass)
    fields = [account, new_pass]
    with open(fname, 'a') as csvfile:
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
            get_password_from_file(DATAFILE, args.get_pass, args.print_to_screen)
        elif args.new_account is not None:
            create_new_account(DATAFILE, args.new_account, args.password_length)
        elif args.get_pass is None and args.new_account is None:
            print("Error. Must give an argument.")
            parser.print_help()
    except RuntimeError as err:
        print(err)
