"""
Unit tests for ezpass.py and related modules
"""

import ezpass

import unittest
import pyperclip
import random
import os

fname = "test_file.csv"
FILE_PASSWORD = "hello"
#! TODO: consider whether it would be better to use a different alphabet from program default?
test_alphabet = ezpass.ALPHABET
password_length = 2 * len(ezpass.ALPHABET)
specified_pass = "myn3wpass"
pwfile = None
acname = "some@gmail.com"


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up for test by creating a new file for passwords and accounts, and populating the file
        with three accounts
        :return: None
        :side effect: new file for passwords and accounts, populated with three accounts
        """
        print("Tests setUp: begin")
        # check if file 'fname' already exists each time before test runs. If it does, delete it.
        if os.path.isfile(fname):
            os.remove(fname)
        global pwfile, acname
        pwfile = ezpass.PwFile.create_new_file(fname, FILE_PASSWORD, True)
        ac1 = ezpass.Account(pwfile, "Twitter")
        ac1.create_new_account(acname, test_alphabet, 8)
        ac2 = ezpass.Account(pwfile, "Gmail")
        ac2.create_new_account(acname, test_alphabet, 8)
        ac3 = ezpass.Account(pwfile, "Pinterest")
        ac3.create_new_account(acname, test_alphabet, 8)
        print("Tests setUp: end")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up after test by deleting file containing passwords and accounts
        :return:
        """
        print("Tests tearDown: begin")
        # check if file 'fname' exists at the beginning of each teardown. If it doesn't throw error.
        if not os.path.isfile(fname):
            raise RuntimeError("Error: File {} does not exist.".format(fname))
        os.remove(fname)
        print("Tests tearDown: end")

    def create_random_fname(self):
        length = random.randint(3, 10)
        random_fname = ""
        for i in range(length):
            letter = ezpass.generate_random_letter(ezpass.ALPHABET)
            random_fname = random_fname + letter
        full_random_fname = random_fname + '.csv'
        return full_random_fname

    def get_non_existing_fname(self):
        random_fname = self.create_random_fname()
        if os.path.isfile(random_fname):
            self.get_non_existing_fname()
        else:
            return random_fname

    def create_random_account(self):
        # ! TODO: create static func from this method?
        # create account length from 3-10
        length = random.randint(3, 10)
        # create a random string of specified length using letters in alphabet
        random_account = ""
        for i in range(length):
            letter = ezpass.generate_random_letter(ezpass.ALPHABET)
            random_account = random_account + letter
        return random_account

    def get_non_existing_account(self, fname):
        """
        Given a filename, returns an account that does not already exist
        :param fname: Name of file with accounts & passwords
        :return: Account instance
        """
        random_account = self.create_random_account()
        global pwfile
        account = ezpass.Account(pwfile, random_account)
        if account.check_if_org_exists():
            return self.get_non_existing_account(fname)
        else:
            return account

    ###############################################################

    #! TODO: consider if it would be better to use ALPHABET
    def test_generate_random_letter(self):
        letter = ezpass.generate_random_letter(test_alphabet)
        self.assertEqual(len(letter), 1)
        self.assertIn(letter, test_alphabet)

    def test_create_password(self):
        alphabet = test_alphabet
        length = random.randint(1, (2 * len(ezpass.ALPHABET)))
        password = ezpass.create_password(alphabet, length)
        self.assertEqual(len(password), length)
        #! TODO: consider whether to check if letter in alphabet (for tests) rather than ezpass.ALPHABET
        for letter in password:
            self.assertIn(letter, ezpass.ALPHABET)

    def test_check_if_account_exists_existing_acct(self):
        pwfile = ezpass.PwFile(fname, FILE_PASSWORD, True)
        account = ezpass.Account(pwfile, 'Twitter')
        ret = account.check_if_org_exists()
        self.assertEqual(ret, True)

    def test_check_if_account_exists_non_existing_acct(self):
        account = self.get_non_existing_account(fname)
        ret = account.check_if_org_exists()
        self.assertEqual(ret, False)

    def test_get_password_from_file_invalid_acct_default(self):
        account = self.get_non_existing_account(fname)
        try:
            # print_to_screen is False
            account.get_password_from_file(False)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework

    # not testing get_password_from_file() with print_to_screen option for valid or invalid accounts

    def test_create_new_account_existing_acct(self):
        # pwfile = ezpass.PwFile(fname, FILE_PASSWORD, True)
        global acname
        account = ezpass.Account(pwfile, "Gmail")
        try:
            account.create_new_account(acname, test_alphabet, password_length)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework

    def test_create_new_account_non_existing_acct(self):
        global acname
        account = self.get_non_existing_account(fname)
        ret = account.check_if_org_exists()
        self.assertEqual(ret, False)
        account.create_new_account(acname, test_alphabet, password_length)
        ret = account.check_if_org_exists()
        self.assertEqual(ret, True)

    def test_delete_account_existing(self):
        global acname
        account = self.get_non_existing_account(fname)
        account.create_new_account(acname, test_alphabet, password_length)
        account.delete_account()
        ret = account.check_if_org_exists()
        self.assertEqual(ret, False)

    def test_delete_account_non_existing(self):
        account = self.get_non_existing_account(fname)
        try:
            account.delete_account()
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_change_password_existing_rand(self):
        global acname
        account = self.get_non_existing_account(fname)
        account.create_new_account(acname, test_alphabet, password_length)
        # print_to_screen is False
        account.get_password_from_file(False)
        pw1 = pyperclip.paste()
        account.set_acpass_rand(test_alphabet, password_length)
        account.get_password_from_file(False)
        pw2 = pyperclip.paste()
        self.assertNotEqual(pw1, pw2)

    def test_change_password_existing_specified_pass(self):
        global acname
        account = self.get_non_existing_account(fname)
        account.create_new_account(acname, test_alphabet, password_length)
        # print_to_screen is False
        account.get_password_from_file(False)
        pw1 = pyperclip.paste()
        account.set_acpass(specified_pass)
        account.get_password_from_file(False)
        pw2 = pyperclip.paste()
        self.assertNotEqual(pw1, pw2)
        self.assertEqual(pw2, specified_pass)

    def test_change_password_non_existing_rand(self):
        account = self.get_non_existing_account(fname)
        try:
            account.set_acpass_rand(test_alphabet, password_length)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_change_password_non_existing_specified_pass(self):
        account = self.get_non_existing_account(fname)
        try:
            account.set_acpass(specified_pass)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_create_new_file_existing(self):
        fname = "test_file.csv"
        try:
            # encrypt = True set arbitrarily
            ezpass.PwFile.create_new_file(fname, FILE_PASSWORD, True)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_create_new_file_non_existing(self):
        fname2 = self.get_non_existing_fname()
        ret = os.path.isfile(fname2)
        self.assertEqual(ret, False)
        # encrypt = True is set arbitrarily
        ezpass.PwFile.create_new_file(fname2, FILE_PASSWORD, True)
        ret = os.path.isfile(fname2)
        self.assertEqual(ret, True)
        os.remove(fname2)


if __name__ == '__main__':
    unittest.main()
