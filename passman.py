import csv
import pyperclip
import argparse
import random
import os.path
# imports for crypto
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# Make sure that datafile is left with new line at the end so new account & password can be added correctly

ENCRYPT = True


class Account:

    def __init__(self, fname, acname):
        """
        :param fname: name of file containing accounts & passwords
        :param acname: account name
        """
        self.fname = fname
        self.acname = acname

    def _readFile(self):
        if ENCRYPT:
            contents = decrypt_file(self.fname)
            data = []
            rows = contents.split('\n')
            for r in rows:
                data.append(r.split(','))
        else:
            with open(self.fname, "r", encoding='utf-8-sig') as file:
                data = list(csv.reader(file))
        return data

    def _writeFile(self, data):
        if ENCRYPT:
            encrypt_file(self.fname, data)
        else:
            with open(self.fname, "w") as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)
        return

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
        data = self._readFile()
        # write out the password file except the account to delete
        new_data = [row for row in data if row[0] != self.acname]
        self._writeFile(new_data)
        return

    def change_password(self, alphabet, password_length):
        """
        Changes password of specified file to a new password of specified length from ALPHABET
        Assumes account name exists in file
        Assumes password length is integer > 0
        :param alphabet: string of full alphabet
        :param password_length: length of password
        :return: None
        side effect: file with new password for specified account
        """
        if not self.check_if_account_exists():
            raise RuntimeError("Account '{}' does not exist".format(self.acname))
        new_password = create_password(alphabet, password_length)
        # read in the password file
        data = self._readFile()
        for row in data:
            if row[0].strip() == self.acname:
                row[1] = new_password
        self._writeFile(data)
        return

    def check_if_account_exists(self):
        """
        If account exists in file, returns True. If account doesn't exist in file, returns False.
        """
        account_header = 'Account-name'
        password_header = 'Password'

        data = self._readFile()
        print(data)
        for row in data:
            if row[0].strip() == self.acname:
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

        data = self._readFile()
        for row in data:
            if row[0].strip() == self.acname:
                password = row[1].strip()
                if password == "":
                    print("Password field is empty for account '{}'".format(self.acname))
                    # ! TODO: what needed to here so 'pw in print buffer' message from mainfunc doesn't print?
                else:
                    if print_to_screen:
                        print("Password for account '{}' is '{}'".format(self.acname, password))
                    else:
                        pyperclip.copy(password)
                return
        raise RuntimeError("Account '{}' not in file".format(self.acname))

    def create_new_account(self, alphabet, password_length):
        """
        For an account name that does not already exist in the file, appends the account name and password to the file
        :param alphabet: string of the full alphabet
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
        data = self._readFile()
        fields = [self.acname, new_pass]
        data.append(fields)
        self._writeFile(data)
        return


def create_new_file(fname):
    """
    Given a file name, creates a new .csv file with that name, and with header columns Account and Password
    Assumes that the file name doesn't already exist in the current directory
    :return: none
    :side effect: .csv file with specified file name, and with header columns Account and Password
    """
    # ! TODO: add an option to overwrite file or enter new fname
    # ! TODO: figure out best way to ensure that filename is desired format (e.g. .csv) catch error or append ending?
    if os.path.isfile(fname):
        raise RuntimeError("File '{}' already exists".format(fname))
    # ! TODO: discuss if makes more sense to use Writer or DictWriter
    fieldnames = ['Account-name', 'Password']
    if ENCRYPT:
        # make fieldnames list of lists to match data in ecrypt file
        encrypt_file(fname, [fieldnames])
    else:
        with open(fname, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    return


def generate_random_letter(alphabet):
    """
    Generates random letter from alphabet
    :param alphabet: string representing full alphabet
    :return: one random letter from the alphabet
    """
    index = random.randint(0, len(alphabet) - 1)
    letter = alphabet[index]
    return letter


def create_password(alphabet, length):
    """
    Creates a password of specified length using letters from ALPHABET
    :param alphabet: string representing full alphabet
    :param length: length of password - an integer > 0
    :return: a password of specified length using letters from ALPHABET
    """
    assert (length > 0)
    password = ""
    for i in range(length):
        letter = generate_random_letter(alphabet)
        password = password + letter
    return password


def encrypt_file(fname, data):
    # Takes data - plain text in memory
    # Transform data into a string
    dataStr = ''
    for elem in data:
        row = (','.join(elem))
        dataStr = dataStr + row + '\n'
    # Alternatively, with list comprehension: dataStr = '\n'.join(','.join(row) for row in data)
    encodedData = dataStr.encode()

    # pass = mypass
    # password = input("Enter password: ")
    password = 'hello'
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
    cipher_text = f.encrypt(encodedData)

    with open(fname, "wb") as enc_file:
        enc_file.write(cipher_text)
    return


def decrypt_file(fname):
    # pass = mypass
    # password = input("Enter password: ")
    password = 'hello'
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
    str_message = message.decode()
    return str_message


def mainfunc():
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('-f', '--file', type=str, help='file name', required=True)
    parser.add_argument('-g', '--get-pass', type=str, help='account name')
    parser.add_argument('-n', '--new-account', type=str, help='new account name')
    parser.add_argument('-p', '--print-to-screen', action='store_true', help='print password to screen', required=False,
                        default=False)
    parser.add_argument('-l', '--password-length', type=int, help='password length', required=False, default=8)
    parser.add_argument('-d', '--delete-account', type=str, help='delete specified account')
    parser.add_argument('-c', '--change-pass', type=str, help='change password for specified account')
    parser.add_argument('-newf', '--new-file', action='store_true', help='whether or not to create new file')
    parser.add_argument('-e', '--encrypt', action='store_true', help='whether or not file is encrypted')
    parser.add_argument('--alphabet', type=str, help='full alphabet')
    args = parser.parse_args()

    assert args.file is not None
    fname = args.file
    global ENCRYPT
    ENCRYPT = args.encrypt

    print(args)

    get_pass_int = int(args.get_pass is not None)
    new_account_int = int(args.new_account is not None)
    delete_account_int = int(args.delete_account is not None)
    change_pass_int = int(args.change_pass is not None)
    new_file_int = int(args.new_file is True)
    param_sum = get_pass_int + new_account_int + delete_account_int + change_pass_int + new_file_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_help()
        raise RuntimeError("Error. Must apply at least one flag")

    if args.get_pass is not None:
        account = Account(fname, args.get_pass)
        account.get_password_from_file(args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(args.get_pass))
    elif args.new_account is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(fname, args.new_account)
        print("Creating new account with", args.new_account)
        account.create_new_account(ALPHABET, args.password_length)
        print("Account created")
    elif args.delete_account is not None:
        account = Account(fname, args.delete_account)
        account.delete_account()
        print("Deleted account:", args.delete_account)
    elif args.change_pass is not None:
        account = Account(fname, args.change_pass)
        account.change_password(ALPHABET, args.password_length)
        print("Password changed for account:", args.change_pass)
    elif args.new_file is True:
        create_new_file(fname)
        print("New file created:", args.new_file)
    return


if __name__ == "__main__":
    mainfunc()
