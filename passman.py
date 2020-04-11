'''
Test with:
python3 getpass.py bird
'''

import csv
import pyperclip
import argparse
import random
import os.path
# imports for crypto below
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DATAFILE = 'cl_test_file.csv'
# Make sure that datafile is left with new line at the end so new account & password can be added correctly


class Account:

    def __init__(self, fname, acname):
        """
        :param fname: name of file containing accounts & passwords
        :param acname: account name
        """
        self.fname = fname
        self.acname = acname

    def get_fname(self):
        return self.fname

    def get_acname(self):
        return self.acname

    def delete_account(self):
        """
        Deletes the specified account name and password
        Assumes account name exists in the file
        :return: None
        :side effect: file without account name and password
        """
        if not self.check_if_account_exists():
            raise RuntimeError("Account '{}' does not exist".format(self.acname))
        # read in the password file
        with open(self.fname, "r") as file:
            data = list(csv.reader(file))
        # write out the password file except the account to delete
        with open(self.fname, "w") as file:
            writer = csv.writer(file)
            for row in data:
                if row[0] != self.acname:
                    writer.writerow(row)
        return

    def change_password(self, alphabet, password_length):
        """
        Changes password of specified file to a new password of specified length from ALPHABET
        Assumes account name exists in file
        Assumes password length is integer > 0
        :param password_length: length of password
        :return: None
        side effect: file with new password for specified account
        """
        if not self.check_if_account_exists():
            raise RuntimeError("Account '{}' does not exist".format(self.acname))
        new_password = create_password(alphabet, password_length)
        # read in the password file
        with open(self.fname, "r", encoding='utf-8-sig') as file:
            data = list(csv.reader(file))
        # write out the account rows into file.
        with open(self.fname, "w") as file:
            writer = csv.writer(file)
            # change the password for the specified account to the new password
            for row in data:
                if row[0].strip() == self.acname:
                    row[1] = new_password
                writer.writerow(row)
        return

    def check_if_account_exists(self):
        """
        If account exists in file, returns True. If account doesn't exist in file, returns False.
        """
        account_header = 'Account-name'
        password_header = 'Password'

        with open(self.fname, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for k, v in row.items():
                    # print(k, v)
                    if k == account_header and v.strip() == self.acname:  # Assumes headers are free of extra spaces
                        return True
            return False

    def get_password_from_file(self, print_to_screen):
        """
        Given valid account name in file, puts password for account in paste buffer.
        If optional '--print_to_screen' parameter entered, then password printed to screen instead of put in paste buffer.
        :param print_to_screen: optional parameter to print password to screen
        :return: None
        :side effect: password in paste buffer (default) or printed to screen (if optional parameter used)
        """
        account_header = 'Account-name'
        password_header = 'Password'

        with open(self.fname, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for k, v in row.items():
                    # print(k, v)
                    if k == account_header and v.strip() == self.acname:  # Assumes headers are free of extra spaces
                        password = row[password_header].strip()
                        if print_to_screen:
                            print("Password for account '{}' is '{}'".format(self.acname, password))
                        else:
                            pyperclip.copy(password)
                            # !TODO: discuss - moved line below to mainfunc()
                            # print("Password for account '{}' in paste buffer".format(account))
                        return
        raise RuntimeError("Account '{}' not in file".format(self.acname))

    def create_new_account(self, alphabet, password_length):
        """
        For an account name that does not already exist in the file, appends the account name and password to the file
        :param password_length: length of password - an integer > 0
        :return: None
        :side effect: account name and password appended to existing file
        """
        assert (password_length > 0)
        if self.check_if_account_exists():
            raise RuntimeError("Account '{}' already exists".format(self.acname))
        new_pass = create_password(alphabet, password_length)
        # !TODO: disc - moved line below to mainfunc() - needed to remove new_pass param
        # !TODO: would it be helpful/important to print password to screen? Thinking not
        # print("Creating new account with", account, new_pass)
        fields = [self.acname, new_pass]
        with open(self.fname, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
        return


def create_new_file(fname):
    """
    Given a file name, creates a new .csv file with that name, and with header columns Account and Password
    Assumes that the file name doesn't already exist in the current directory
    :return: none
    :side effect: .csv file with specified file name, and with header columns Account and Password
    """
    #! TODO: add an option to overwrite file or enter new fname
    #! TODO: figure out best way to ensure that filename is desired format (e.g. .csv) catch error or append ending?
    if os.path.isfile(fname):
        raise RuntimeError("File '{}' already exists".format(fname))
    #! TODO: discuss if makes more sense to use Writer or DictWriter
    with open(fname, 'w', newline='') as csvfile:
        fieldnames = ['Account-name', 'Password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    return


def generate_random_letter(alphabet):
    """
    Generates random letter from alphabet
    :param alphabet: string representing full alphabet
    :return: one random letter from the alphabet
    """
    index = random.randint(0, len(alphabet)-1)
    letter = alphabet[index]
    return letter


def create_password(alphabet, length):
    """
    Creates a password of specified length using letters from ALPHABET
    :param alphabet: string representing full alphabet
    :param length: length of password - an integer > 0
    :return: a password of specified length using letters from ALPHABET
    """
    assert(length > 0)
    password = ""
    for i in range(length):
        letter = generate_random_letter(alphabet)
        password = password + letter
    return password


def encrypt_file(fname):
    with open(fname, 'r') as orig_file:
        text = orig_file.read()
        encodedText = text.encode()

    # pass = mypass
    password = input("Enter password: ")
    encodedPassword = password.encode()

    # salt = os.urandom(16)
    salt = b"1\xf6I\xf3\xce\xd4\x02^\x94\xbe\xb0\xe4\x8bO\x04\x1d"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
     )
    key = base64.urlsafe_b64encode(kdf.derive(encodedPassword))
    f = Fernet(key)
    cipher_text = f.encrypt(encodedText)
    print(cipher_text)

    enc_fname = fname + ".enc"

    with open(enc_fname, "wb") as enc_file:
        enc_file.write(cipher_text)

    print("Finished writing encrypted file")


def decrypt_file(fname):
    # pass = mypass
    password = input("Enter password: ")
    encodedPassword = password.encode()

    # salt = os.urandom(16)
    salt = b'1\xf6I\xf3\xce\xd4\x02^\x94\xbe\xb0\xe4\x8bO\x04\x1d'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(encodedPassword))
    f = Fernet(key)

    with open(fname, "r") as enc_file:
        cipher_text = enc_file.read()

    enc_cipher_text = cipher_text.encode()
    message = f.decrypt(enc_cipher_text)
    print(message)


def mainfunc():
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('--get-pass', type=str, help='account name')
    parser.add_argument('--new-account', type=str, help='new account name')
    parser.add_argument('--print-to-screen', action='store_true', help='print password to screen', required=False,
                        default=False)
    parser.add_argument('--password-length', type=int, help='password length', required=False, default=8)
    parser.add_argument('--delete-account', type=str, help='delete specified account')
    parser.add_argument('--change-pass', type=str, help='change password for specified account')
    parser.add_argument('--new-file', type=str, help='create new file for passwords')
    parser.add_argument('--alphabet', type=str, help='full alphabet')
    args = parser.parse_args()
    print(args)

    get_pass_int = int(args.get_pass is not None)
    new_account_int = int(args.new_account is not None)
    delete_account_int = int(args.delete_account is not None)
    change_pass_int = int(args.change_pass is not None)
    new_file_int = int(args.new_file is not None)
    param_sum = get_pass_int + new_account_int + delete_account_int + change_pass_int + new_file_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_help()
        raise RuntimeError("Error. Must apply at least one flag")

    if args.get_pass is not None:
        account = Account(DATAFILE, args.get_pass)
        account.get_password_from_file(args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(args.get_pass))
    elif args.new_account is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(DATAFILE, args.new_account)
        print("Creating new account with", args.new_account)
        account.create_new_account(ALPHABET, args.password_length)
        print("Account created")
    elif args.delete_account is not None:
        account = Account(DATAFILE, args.delete_account)
        account.delete_account()
        print("Deleted account:", args.delete_account)
    elif args.change_pass is not None:
        account = Account(DATAFILE, args.change_pass)
        account.change_password(ALPHABET, args.password_length)
        print("Password changed for account:", args.change_pass)
    elif args.new_file is not None:
        create_new_file(args.new_file)
        print("New file created:", args.new_file)
    return


if __name__ == "__main__":
    mainfunc()
