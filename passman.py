import shlex
import pyperclip
import argparse
import random
import os.path
import pickle
import cmd
import sys
# imports for encryption
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Make sure that datafile is left with new line at the end so new account & password can be added correctly

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


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
            decryptedMessage = self._decryptFile()
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
            self._encryptFile(data)
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
    def create_new_file(fname: str, fpass: str, encrypt: bool):
        """
        Given a file name, password and encryption value, creates a new file with those values and an empty
        list for storing accounts
        Assumes that the file name doesn't already exist in the current directory
        :return: PwFile  instance
        :side effect: new file with specified file name, password and encryption value
        """
        # ! TODO: add an option to overwrite file or enter new fname
        # ! TODO: what's best  way to ensure that file is desired format?
        # ! TODO: Check this func
        if os.path.isfile(fname):
            raise RuntimeError("File '{}' already exists".format(fname))
        fd = os.open(fname, os.O_CREAT)
        os.close(fd)
        new_file = PwFile(fname, fpass, encrypt)
        new_file.writeFile([])
        return new_file

#! TODO - rename class to AcList?
#! TODO - take acname out of class?
#! TODO - rename acname to username?
#
# class AccountDB:
#     def __init__(self, pwfile: PwFile) -> None:
#         """
#         :param pwfile: PwFile instance
#         :param org: name of organization that account belongs to (e.g. Bank of America)
#         # :param acname: account name (cannot contain spaces, newlines or tabs)
#         """
#         assert pwfile is not None
#         self.pwfile = pwfile
#         # TODO read the pwfile,
#         # populate a local representation of the accounts
#         self.accounts = self.pwfile.readFile()
#
#     def get_account_pass(self, orgname):
#         # 1. find account with orgname
#         # 2. print/copy account's username/pass


class Account:
    def __init__(self, pwfile: PwFile, org: str) -> None:
        """
        :param pwfile: PwFile instance
        :param org: name of organization that account belongs to (e.g. Bank of America)
        # :param acname: account name (cannot contain spaces, newlines or tabs)
        """
        assert pwfile is not None
        if not Account.validate_orgname(org):
            raise RuntimeError("Org format is invalid")
        self.pwfile = pwfile
        self.org = org
        self.acname = None
        self.acpassword = None

    @staticmethod
    def validate_accountname(acname):
        return Account._validate_string(acname)

    @staticmethod
    def validate_orgname(org):
        return Account._validate_string(org)

    @staticmethod
    def validate_pass(pw):
        return Account._validate_string(pw)

    @staticmethod
    def _validate_string(s):
        '''
        Returns True if the string is a non-empty string with no whitespaces
        :param s: string to validate
        :return: True if s is valid
        '''
        if (s is None) or (s == "") or (" " in s) or (s.strip() != s):
            return False
        return True

    def get_acname(self):
        return self.acname

    def get_org(self):
        return self.org

    def delete_account(self):
        """
        Deletes the specified account name and password
        Assumes account name exists in the file
        :return: None
        :side effect: file without account name and password
        """
        if not self.check_if_org_exists():
            raise RuntimeError("Account for org '{}' does not exist".format(self.org))
        # read in the password file
        data = self.pwfile.readFile()
        # write out the password file except the account to delete
        new_data = [account for account in data if account.org != self.org]
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

    def set_acpass(self, specified_pass: str) -> None:
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
        if not self.check_if_org_exists():
            raise RuntimeError("Account for org '{}' does not exist".format(self.org))
        if not Account.validate_pass(new_password):
            raise RuntimeError("Invalid password format")
        # read in the password file
        aclist = self.pwfile.readFile()
        for account in aclist:
            if account.org == self.org:
                account.acpassword = new_password
        self.pwfile.writeFile(aclist)
        return

    def check_if_org_exists(self) -> bool:
        """
        If account exists in file, returns True. If account doesn't exist in file, returns False.
        """
        aclist = self.pwfile.readFile()
        for account in aclist:
            if account.org == self.org:
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
        aclist = self.pwfile.readFile()
        for account in aclist:
            if account.org == self.org:
                username = account.acname
                password = account.acpassword
                print("Username for org {} is {}".format(self.org, username))
                if print_to_screen:
                    print("Password for org '{}' is '{}'".format(self.org, password))
                else:
                    pyperclip.copy(password)
                return
        raise RuntimeError("Account for org '{}' not in file".format(self.org))

    def create_new_account(self, acname: str, alphabet: str, password_length: bool) -> None:
        """
        For an account name that does not already exist in the file, appends the account name and password to the file
        :acname: username
        :param alphabet: string of the full alphabet
        :param password_length: length of password - an integer > 0
        :return: None
        :side effect: account name and password appended to existing file
        """
        assert (password_length > 0)
        if not Account.validate_accountname(acname):
            raise RuntimeError("Account name {} has an invalid format".format(acname))
        if self.check_if_org_exists():
            raise RuntimeError("Account for org '{}' already exists".format(self.org))
        self.acpassword = create_password(alphabet, password_length)
        self.acname = acname
        aclist = self.pwfile.readFile()
        aclist.append(self)
        self.pwfile.writeFile(aclist)
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


class PassShell(cmd.Cmd):
    intro = 'Welcome to the Passman interactive shell.   Type "help" or "?" to list commands.\n'
    prompt = '(passman) '
    file = None

    def __init__(self, pfile):
        cmd.Cmd.__init__(self, 'tab', sys.stdin, sys.stdout)
        self.pfile = pfile

    # ----- basic passman commands -----
    # Must have pwfile before interactive mode can be used

    #! TODO improve docstrsing help for new_account
    def do_new_account(self, line):
        """Add a new org:  NEW_ACCOUNT --org-name --pw-length --set-acpass"""
        parser = argparse.ArgumentParser()
        parser.add_argument('-on', '--org-name', type=str, help='new org name')
        parser.add_argument('-pl', '--pw-length', type=int, required=False, default=8, help='password length')
        parser.add_argument('-sp', '--set-acpass', type=str, default=None, help='set specified password')
        args = parser.parse_args(shlex.split(line))

        if args.pw_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(self.pfile, args.org_name)
        print("Creating new account for:", args.org_name)
        acname = input("Enter username: ")
        account.create_new_account(acname, ALPHABET, args.pw_length)
        if args.set_acpass is not None:
            account.set_acpass(args.set_acpass)
        print("Account created for:", args.org_name)

    def do_delete_account(self, acname):
        """Delete account for specified org:  D acname"""
        account = Account(self.pfile, acname)
        account.delete_account()
        print("Deleted account for: ", acname)

    def do_get_account_password(self, acname, print_to_screen):
        """Get password for specified org: G org_name print_to_screen"""
        account = Account(self.pfile, acname)
        account.get_password_from_file(print_to_screen)
        if print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(acname))

    def do_change_account_password(self, acname, set_acpass, password_length):
        """Change password for specified org: CP acname set_acpass password_length"""
        account = Account(self.pfile, acname)
        if set_acpass is None:
            account.set_acpass_rand(ALPHABET, password_length)
        else:
            account.set_acpass(acname)
        print("Password changed for account: ", acname)

    def do_quit(self, arg):
        """Quit the program"""
        print(arg)


def mainfunc():
    parser = argparse.ArgumentParser(description='Retrieve password.')
    # required
    parser.add_argument('-f', '--file', type=str, help='file name', required=True)
    # choose one
    parser.add_argument('-g', '--get-acpass', type=str, help='org name')
    parser.add_argument('-na', '--new-account', type=str, help='new org name')
    parser.add_argument('-d', '--delete-account', type=str, help='delete account for specified org')
    parser.add_argument('-nf', '--new-file', action='store_true', help='whether or not to create new file')
    parser.add_argument('-cp', '--change-acpass', type=str, help='org to change password for')
    parser.add_argument('-sp', '--set-acpass', type=str, help='set specified password', default=None)
    # optional
    parser.add_argument('-print', '--print-to-screen', action='store_true', help='print password to screen',
                        required=False, default=False)
    parser.add_argument('-l', '--password-length', type=int, help='password length', required=False, default=8)
    parser.add_argument('-e', '--encrypt', action='store_true', help='whether or not file is encrypted')
    parser.add_argument('-a', '--alphabet', type=str, help='full alphabet', required=False)
    parser.add_argument('-i', '--interactive', action='store_true', help='whether or not to use '
                                                                         'interactive mode')

    args = parser.parse_args()

    assert args.file is not None
    fname = args.file

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
    interactive_int = int(args.interactive is True)
    param_sum = get_acpass_int + new_account_int + delete_account_int + change_acpass_int + new_file_int + interactive_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_help()
        raise RuntimeError("Error. Must use --file and at least one additional flag")

    if args.new_file is True:
        PwFile.create_new_file(fname, password, args.encrypt)
        print("New file created:", fname)
        return

    # Create PwFile instance based on file name & password
    pfile = PwFile(fname, password, args.encrypt)

    if args.interactive is True:
        shell = PassShell(pfile)
        shell.cmdloop()
        return

    if args.get_acpass is not None:
        account = Account(pfile, args.get_acpass)
        account.get_password_from_file(args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(args.get_acpass))
    elif args.new_account is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(pfile, args.new_account)
        print("Creating new account for:", args.new_account)
        acname = input("Enter username: ")
        account.create_new_account(acname, ALPHABET, args.password_length)
        if args.set_acpass is not None:
            account.set_acpass(args.set_acpass)
        print("Account created")
    elif args.delete_account is not None:
        account = Account(pfile, args.delete_account)
        account.delete_account()
        print("Deleted account for:", args.delete_account)
    elif args.change_acpass is not None:
        account = Account(pfile, args.change_acpass)
        if args.set_acpass is None:
            account.set_acpass_rand(ALPHABET, args.password_length)
        else:
            account.set_acpass(args.set_acpass)
        print("Password changed for account:", args.change_acpass)
    return


if __name__ == "__main__":
    mainfunc()
