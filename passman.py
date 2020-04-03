'''
Test with:
python3 getpass.py bird
'''

import csv
import pyperclip
import argparse
import random

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DATAFILE = 'test_file.csv'
# Make sure that datafile is left with new line at the end so new account & password can be added correctly


def get_password_from_file(fname, account, print_to_screen):
    """
    Given valid account name in file, puts password for account in paste buffer.
    If optional '--print_to_screen' parameter entered, then password printed to screen instead of put in paste buffer.
    :param fname: name of file containing accounts & passwords
    :param account: account name
    :param print_to_screen: optional parameter to print password to screen
    :return: None
    :side effect: password in paste buffer (default) or printed to screen (if optional parameter used)
    """
    account_header = 'Account-name'
    password_header = 'Password'

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
                        #!TODO: discuss - moved line below to mainfunc()
                        # print("Password for account '{}' in paste buffer".format(account))
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
    """
    Creates a password of specified length using letters from ALPHABET
    :param length: length of password - an integer > 0
    :return: a password of specified length using letters from ALPHABET
    """
    assert(length > 0)
    password = ""
    for i in range(length):
        letter = generate_random_letter(ALPHABET)
        password = password + letter
    return password


def create_new_account(fname, account, password_length):
    """
    For an account name that does not already exist in the file, appends the account name and password to the file
    :param fname: name of file containing account & passwords
    :param account: name of account to be created
    :param password_length: length of password - an integer > 0
    :return: None
    :side effect: account name and password appended to existing file
    """
    assert(password_length > 0)
    if check_if_account_exists(fname, account):
        raise RuntimeError("Account '{}' already exists".format(account))
    new_pass = create_password(password_length)
    #!TODO: disc - moved line below to mainfunc() - needed to remove new_pass param
    #!TODO: would it be helpful/important to print password to screen? Thinking not
    # print("Creating new account with", account, new_pass)
    fields = [account, new_pass]
    with open(fname, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
    return


def delete_account(fname, account):
    """
    Deletes the specified account name and password
    Assumes account name exists in the file
    :param fname: name of file containing account & passwords
    :param account: name of account to be deleted
    :return: None
    :side effect: file without account name and password
    """
    if not check_if_account_exists(fname, account):
        raise RuntimeError("Account '{}' does not exist".format(account))
    # read in the password file
    with open(fname, "r") as file:
        data = list(csv.reader(file))
    # write out the password file except the account to delete
    with open(fname, "w") as file:
        writer = csv.writer(file)
        for row in data:
            if row[0] != account:
                writer.writerow(row)
    return


def change_password(fname, account, password_length):
    """
    Changes password of specified file to a new password of specified length from ALPHABET
    Assumes account name exists in file
    Assumes password length is integer > 0
    :param fname: name of file containing account & passwords
    :param account: name of account for which password to be changed
    :param password_length: length of password
    :return: None
    side effect: file with new password for specified account
    """
    if not check_if_account_exists(fname, account):
        raise RuntimeError("Account '{}' does not exist".format(account))
    new_password = create_password(password_length)
    # read in the password file
    with open(fname, "r", encoding='utf-8-sig') as file:
        data = list(csv.reader(file))
    # write out the account rows into file.
    with open(fname, "w") as file:
        writer = csv.writer(file)
        # change the password for the specified account to the new password
        for row in data:
            if row[0].strip() == account:
                row[1] = new_password
            writer.writerow(row)
    return


def mainfunc():
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('--get-pass', type=str, help='account name')
    parser.add_argument('--new-account', type=str, help='new account name')
    parser.add_argument('--print-to-screen', action='store_true', help='print password to screen', required=False,
                        default=False)
    parser.add_argument('--password-length', type=int, help='password length', required=False, default=8)
    parser.add_argument('--delete-account', type=str, help='delete specified account')
    parser.add_argument('--change-pass', type=str, help='change password for specified account')
    args = parser.parse_args()
    print(args)

    get_pass_int = int(args.get_pass is not None)
    new_account_int = int(args.new_account is not None)
    delete_account_int = int(args.delete_account is not None)
    change_pass_int = int(args.change_pass is not None)
    param_sum = get_pass_int + new_account_int + delete_account_int + change_pass_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_help()
        raise RuntimeError("Error. Must apply at least one flag")
    if args.get_pass is not None:
        get_password_from_file(DATAFILE, args.get_pass, args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(args.get_pass))
    elif args.new_account is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        print("Creating new account with", args.new_account)
        create_new_account(DATAFILE, args.new_account, args.password_length)
        print("Account created")
    elif args.delete_account is not None:
        delete_account(DATAFILE, args.delete_account)
        print("Deleted account:", args.delete_account)
    elif args.change_pass is not None:
        change_password(DATAFILE, args.change_pass, args.password_length)
        print("Password changed for account:", args.change_pass)


if __name__ == "__main__":
    mainfunc()

