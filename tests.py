import getpass
import unittest
import pyperclip
import random

fname = 'test-file.csv'


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

    def get_non_existing_account(self):
        # create account length from 3-10
        length = random.randint(3, 10)
        # create a random string of specified length using letters in alphabet
        random_account = ""
        for i in range(length):
            letter = getpass.generate_random_letter(getpass.ALPHABET)
            random_account = random_account + letter
        if getpass.check_if_account_exists(fname, random_account):
            return self.create_random_account()
        else:
            return random_account

    def test_create_new_account(self):
        password_length = 2 * len(getpass.ALPHABET)
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


if __name__ == '__main__':
    unittest.main()