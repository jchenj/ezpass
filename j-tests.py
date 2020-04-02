import getpass
import unittest
import pyperclip
import random

fname = 'test-file.csv'
password_length = 2 * len(getpass.ALPHABET)


class Tests(unittest.TestCase):

    def test_generate_random_letter(self):
        letter = getpass.generate_random_letter('abcd')
        self.assertEqual(len(letter), 1)
        self.assertIn(letter, 'abcd')

    def test_check_if_account_exists(self):
        account = 'bird'
        # existing account
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, True)
        # non-existing account
        account = 'pig'
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, False)

    def test_get_password_from_file(self):
        account = 'bird'
        password = "feathers"
        # valid account - default
        getpass.get_password_from_file(fname, account, False)
        pw = pyperclip.paste()
        self.assertEqual(pw, password)
        # not testing valid account - print screen
        account = 'pig'
        # invalid account - default
        try:
            getpass.get_password_from_file(fname, account, False)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework
        # not testing invalid account - print to screen

    def test_create_password(self):
        length = random.randint(1, (2 * len(getpass.ALPHABET)))
        password = getpass.create_password(length)
        self.assertEqual(len(password), length)
        for letter in password:
            self.assertIn(letter, getpass.ALPHABET)

    def create_random_account(self):
        #! TODO: create static func from this method?
        # create account length from 3-10
        length = random.randint(3, 10)
        # create a random string of specified length using letters in alphabet
        random_account = ""
        for i in range(length):
            letter = getpass.generate_random_letter(getpass.ALPHABET)
            random_account = random_account + letter
        return random_account

    def get_non_existing_account(self):
        random_account = self.create_random_account()
        if getpass.check_if_account_exists(fname, random_account):
            return self.get_non_existing_account()
        else:
            return random_account

    def test_create_new_account(self):
        # account already exists in file
        account = "dog"
        try:
            getpass.create_new_account(fname, account, password_length)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework
        # account doesn't yet exist in file
        account = self.get_non_existing_account()
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, False)
        getpass.create_new_account(fname, account, password_length)
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, True)

    def test_delete_account_existing(self):
        # account exists
        account = self.get_non_existing_account()
        getpass.create_new_account(fname, account, password_length)
        getpass.delete_account(fname, account)
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, False)

    def test_delete_account_non_existing(self):
        # account doesn't exist
        account = self.get_non_existing_account()
        try:
            getpass.delete_account(fname, account)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass



if __name__ == '__main__':
    unittest.main()