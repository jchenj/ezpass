import passman
import unittest
import pyperclip
import random
import os.path

fname = "test_file.csv"
password_length = 2 * len(passman.ALPHABET)


class Tests(unittest.TestCase):

    def create_random_account(self):
        #! TODO: create static func from this method?
        # create account length from 3-10
        length = random.randint(3, 10)
        # create a random string of specified length using letters in alphabet
        random_account = ""
        for i in range(length):
            letter = passman.generate_random_letter(passman.ALPHABET)
            random_account = random_account + letter
        return random_account

    def get_non_existing_account(self, fname):
        '''
        :return:
        :param fname: Name of file with accounts & passwords
        :return: Account instance
        '''
        random_account = self.create_random_account()
        account = passman.Account(fname, random_account)
        if account.check_if_account_exists():
            return self.get_non_existing_account(fname)
        else:
            return account

 ###############################################################

    def test_generate_random_letter(self):
        letter = passman.generate_random_letter('abcd')
        self.assertEqual(len(letter), 1)
        self.assertIn(letter, 'abcd')

    def test_create_password(self):
        length = random.randint(1, (2 * len(passman.ALPHABET)))
        password = passman.create_password(length)
        self.assertEqual(len(password), length)
        for letter in password:
            self.assertIn(letter, passman.ALPHABET)

    def test_check_if_account_exists(self):
        account = passman.Account(fname, 'bird')
        # existing account
        ret = account.check_if_account_exists()
        self.assertEqual(ret, True)
        # non-existing account
        account = passman.Account(fname, 'pig')
        ret = account.check_if_account_exists()
        self.assertEqual(ret, False)

    def test_get_password_from_file(self):
        account = passman.Account(fname, 'bird')
        password = "feathers"
        # valid account - default
        account.get_password_from_file(False)
        pw = pyperclip.paste()
        self.assertEqual(pw, password)
        # not testing valid account - print screen
        account = passman.Account(fname, 'pig')
        # invalid account - default
        try:
            account.get_password_from_file(False)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework
        # not testing invalid account - print to screen

    def test_create_new_account(self):
        # account already exists in file
        account = passman.Account(fname, "dog")
        try:
            account.create_new_account(password_length)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework
        # account doesn't yet exist in file
        account = self.get_non_existing_account(fname)
        ret = account.check_if_account_exists()
        self.assertEqual(ret, False)
        account.create_new_account(password_length)
        ret = account.check_if_account_exists()
        self.assertEqual(ret, True)

    def test_delete_account_existing(self):
        # account exists
        account = self.get_non_existing_account(fname)
        account.create_new_account(password_length)
        account.delete_account()
        ret = account.check_if_account_exists()
        self.assertEqual(ret, False)

    def test_delete_account_non_existing(self):
        # account doesn't exist
        account = self.get_non_existing_account(fname)
        try:
            account.delete_account()
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_change_password_existing(self):
        # account exists
        account = self.get_non_existing_account(fname)
        account.create_new_account(password_length)
        account.get_password_from_file(False)
        pw1 = pyperclip.paste()
        account.change_password(password_length)
        account.get_password_from_file(False)
        pw2 = pyperclip.paste()
        self.assertNotEqual(pw1, pw2)

    def test_change_password_non_existing(self):
        # account doesn't exist
        account = self.get_non_existing_account(fname)
        try:
            account.change_password(password_length)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_create_new_file_existing(self):
        # filename exists in cwd
        fname = "test_file.csv"
        try:
            passman.create_new_file(fname)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_create_new_file_non_existing(self):
        # filename doesn't exist yet in cwd
        #! TODO: replace fname with non-existing account name (once helper funcs added)
        fname = "another_new_file.csv"
        ret = os.path.isfile(fname)
        self.assertEqual(ret, False)
        passman.create_new_file(fname)
        ret = os.path.isfile(fname)
        self.assertEqual(ret, True)


if __name__ == '__main__':
    unittest.main()