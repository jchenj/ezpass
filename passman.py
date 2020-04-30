import pyperclip
import argparse
import random
import os.path
import pickle
# imports for encryption
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Make sure that datafile is left with new line at the end so new account & password can be added correctly

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# ENCRYPT is set as global variable in __main__ func. Also set here because it's needed for testing
ENCRYPT = True


class PwFile:

    def __init__(self, fname: str, fpass: str, encrypt: bool) -> None:
        """
        :param fname: name of file (str)
        :param fpass: password for file fname (str)
        :param encrypt: whether or not file is encrypted (bool)
        """
        if not os.path.isfile(fname):
            raise RuntimeError("File '{}' does not exist".format(fname))
        self.fname = fname
        self.fpass = fpass
        self.encrypt = encrypt

    def _encryptFile(self, data: list) -> None:
        # Pickle data (list of Account instances)
        pickledData = pickle.dumps(data)
        encodedPassword = self.fpass.encode()

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
        cipher_text = f.encrypt(pickledData)

        with open(self.fname, "wb") as enc_file:
            enc_file.write(cipher_text)
        return

    def _decryptFile(self) -> str:
        encodedPassword = self.fpass.encode()

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

        with open(self.fname, "r") as enc_file:
            cipher_text = enc_file.read()

        enc_cipher_text = cipher_text.encode()
        message = f.decrypt(enc_cipher_text)
        return message

    def readFile(self) -> list:
        """
        Opens self.fname and loads data for accounts
        :return: list of Account instances
        """
        if self.encrypt:
            decryptedMessage = self.decrypt_file(self.fname, self.fpass)
            data = pickle.loads(decryptedMessage)
        else:
            with open(self.fname, 'rb') as file:
                data = pickle.load(file)

        return data

    def writeFile(self, data: list) -> None:
        """
        Writes data for accounts to PwFile.fname
        :param data: list of Account instances
        :return: None
        :side effect: updated file
        """
        if self.encrypt:
            self.encrypt_file(self.fname, data, self.fpass)
        else:
            with open(self.fname, 'wb') as file:
                pickle.dump(data, file)
        return

    def get_fname(self) -> str:
        return self.fname

    def get_fpass(self) -> str:
        return self.fpass

    #! TODO: is it correct to have initial check?
    def change_fpass(self, new_password: str) -> None:
        """
        Changes password for file
        :param new_password: new password for file
        :return: None
        :side effect: file updated with new password
        """
        if not self.fpass():
            raise RuntimeError("Password for file '{}' does not exist".format(self.fname))
        if new_password == "":
            raise RuntimeError("Password cannot be empty")
        self.fpass = new_password
        return

    @staticmethod
    def create_new_file(fname: str, fpass: str, encrypt: bool) -> None:
        """
        Given a file name, password and encryption value, creates a new file with those values and an empty
        list for storing accounts
        Assumes that the file name doesn't already exist in the current directory
        :return: none
        :side effect: new file with specified file name, password and encryption value
        """
        # ! TODO: add an option to overwrite file or enter new fname
        # ! TODO: what's best  way to ensure that file is desired format?
        # !  TODO: Check this func
        if os.path.isfile(fname):
            raise RuntimeError("File '{}' already exists".format(fname))

        new_file = PwFile(fname, fpass, encrypt)
        new_file.writeFile([])
        return

#! TODO next - add PWfile instance as param to account
#! TODO - rename class to AcList?
#! TODO - take acname out of class?


class Account:
    def __init__(self, pwfile: PwFile, acname: str) -> None:
        """
        :param pwfile: PwFile instance
        :param acname: account name (cannot contain spaces, newlines or tabs)
        """
        if " " in acname:
            raise RuntimeError("Spaces not allowed in account names")
        self.pwfile = pwfile
        self.acname = acname
        self.acpassword = None

    def get_acname(self):
        return self.acname

    #! TODO: check - do I need to include self.acname in signature?
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
        data = self.pwfile.readFile()
        # write out the password file except the account to delete
        new_data = [account for account in data if account.acname != self.acname]
        self.pwfile.writeFile(new_data)
        return

    def set_acpass_rand(self, alphabet: str, password_length: int) -> None:
        """
        Sets password of account to a new random password of specified length from ALPHABET
        Assumes password length is integer > 0
        :param alphabet: string of full alphabet
        :param password_length: length of password
        :return new_password: string
        """
        new_password = create_password(alphabet, password_length)
        return self._change_password(new_password)

    def set_acpass(self, specified_pass: int) -> None:
        """
        Sets password of specified account to a new specified password
        Assumes account names exists in file
        :param specified_pass: specified new password (string)
        :return: new_password: string
        """
        return self._change_password(specified_pass)

    def _change_password(self, new_password: str) -> None:
        """
        Changes password of specified account to new (pre-set) password
        Assumes account name exists in file
        :param new_password: new password (string)
        :return: None
        :side effect: file with account updated with new password
        """
        if not self.check_if_account_exists():
            raise RuntimeError("Account '{}' does not exist".format(self.acname))
        if new_password == "":
            raise RuntimeError("Password cannot be empty")
        # read in the password file
        data = self.pwfile.readFile()
        for account in data:
            #! TODO: is strip() necessary?
            if account.acname.strip() == self.acname:
                account.acpassword = new_password
        self.pwfile.writeFile(data)
        return

    def check_if_account_exists(self) -> bool:
        """
        If account exists in file, returns True. If account doesn't exist in file, returns False.
        """
        data = self.pwfile.readFile()
        for account in data:
            if account.acname.strip() == self.acname:
                return True
        return False

    def get_password_from_file(self, print_to_screen: bool) -> None:
        """
        Given valid account name in file, puts password for account in paste buffer.
        If optional '--print_to_screen' parameter entered, then password printed to screen instead of put in paste buffer.
        :param print_to_screen: optional parameter to print password to screen
        :return: None
        :side effect: password in paste buffer (default) or printed to screen (if optional parameter used)
        """
        data = self.pwfile.readFile()
        for account in data:
            if account.acname.strip() == self.acname:
                password = account.acpassword.strip()
                if password == "":
                    print("Password field is empty for account '{}'".format(self.acname))
                    # ! TODO: what needed to put here so 'pw in print buffer' message from mainfunc doesn't print?
                else:
                    if print_to_screen:
                        print("Password for account '{}' is '{}'".format(self.acname, password))
                    else:
                        pyperclip.copy(password)
                return
        raise RuntimeError("Account '{}' not in file".format(self.acname))

    def create_new_account(self, alphabet: str, password_length: bool) -> None:
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
        self.acpassword = create_password(alphabet, password_length)
        data = self.pwfile.readFile()
        data.append(self)
        self.pwfile.writeFile(data)
        return


def generate_random_letter(alphabet: str) -> str:
    """
    Generates random letter from alphabet
    :param alphabet: string representing full alphabet
    :return: one random letter from the alphabet
    """
    index = random.randint(0, len(alphabet) - 1)
    letter = alphabet[index]
    return letter


def create_password(alphabet: str, length: int) -> str:
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

def mainfunc():
    parser = argparse.ArgumentParser(description='Retrieve password.')
    parser.add_argument('-f', '--file', type=str, help='file name', required=True)
    parser.add_argument('-g', '--get-acpass', type=str, help='account name')
    parser.add_argument('-na', '--new-account', type=str, help='new account name')
    parser.add_argument('-print', '--print-to-screen', action='store_true', help='print password to screen', required=False,
                        default=False)
    parser.add_argument('-l', '--password-length', type=int, help='password length', required=False, default=8)
    parser.add_argument('-d', '--delete-account', type=str, help='delete specified account')
    parser.add_argument('-nf', '--new-file', action='store_true', help='whether or not to create new file')
    parser.add_argument('-e', '--encrypt', action='store_true', help='whether or not file is encrypted')
    parser.add_argument('-a', '--alphabet', type=str, help='full alphabet', required=False)
    parser.add_argument('-cp', '--change-acpass', type=str, help='account to change password of')
    parser.add_argument('-sp', '--set-acpass', type=str, help='set specified password', default=None)
    args = parser.parse_args()

    assert args.file is not None
    fname = args.file
    global ENCRYPT
    ENCRYPT = args.encrypt
    if args.encrypt:
        password = input("Enter password for file {}: ".format(fname))
    else:
        password = None

    print(args)

    get_acpass_int = int(args.get_acpass is not None)
    new_account_int = int(args.new_account is not None)
    delete_account_int = int(args.delete_account is not None)
    change_acpass_int = int(args.change_acpass is not None)
    new_file_int = int(args.new_file is True)
    param_sum = get_acpass_int + new_account_int + delete_account_int + change_acpass_int + new_file_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_help()
        raise RuntimeError("Error. Must use --file and at least one additional flag")

    if args.new_file is True:
        PwFile.create_new_file(fname, password, ENCRYPT)
        print("New file created:", fname)
        return

    pw = PwFile(fname, password, ENCRYPT)

    if args.get_acpass is not None:
        account = Account(pw, args.get_acpass)
        account.get_password_from_file(args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(args.get_acpass))
    elif args.new_account is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(pw, args.new_account)
        print("Creating new account with", args.new_account)
        account.create_new_account(ALPHABET, args.password_length)
        if args.set_acpass is not None:
            account.set_acpass(args.set_acpass)
        print("Account created")
    elif args.delete_account is not None:
        account = Account(pw, args.delete_account)
        account.delete_account()
        print("Deleted account:", args.delete_account)
    elif args.change_acpass is not None:
        account = Account(pw, args.change_acpass)
        if args.set_acpass is None:
            account.set_acpass_rand(ALPHABET, args.password_length)
        else:
            account.set_acpass(args.set_acpass)
        print("Password changed for account:", args.change_acpass)
    return


if __name__ == "__main__":
    mainfunc()
