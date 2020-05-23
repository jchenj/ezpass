"""
Defines Account class to create and manage accounts within a Pwfile instance in ezpass
"""

import pyperclip

from pwfile import PwFile
from util import create_password


class Account:
    def __init__(self, pwfile: PwFile, org: str) -> None:
        """
        :param pwfile: PwFile instance
        :param org: name of organization that account belongs to (e.g. Bank of America)
        :param acname: account name (cannot contain spaces, newlines or tabs)
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
