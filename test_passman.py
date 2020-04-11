import passman
import unittest
import pyperclip
import random
import os
import csv

#! TODO: should these be allcaps?
fname = "test_file.csv"
#! TODO: would this be better to be passman.ALPHABET?
alphabet = 'abcd'
password_length = 2 * len(passman.ALPHABET)


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
        passman.create_new_file(fname)
        ac1 = passman.Account(fname, "bird")
        ac1.create_new_account(alphabet, 8)
        ac2 = passman.Account(fname, "fish")
        ac2.create_new_account(alphabet, 8)
        ac3 = passman.Account(fname, "dog")
        ac3.create_new_account(alphabet, 8)
        print("Tests setUp: end")

    #! TODO: discuss how to test teardown class method
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
            letter = passman.generate_random_letter(passman.ALPHABET)
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
            letter = passman.generate_random_letter(passman.ALPHABET)
            random_account = random_account + letter
        return random_account

    def get_non_existing_account(self, fname):
        """
        Given a filename, returns an account that does not already exist
        :param fname: Name of file with accounts & passwords
        :return: Account instance
        """
        random_account = self.create_random_account()
        account = passman.Account(fname, random_account)
        if account.check_if_account_exists():
            return self.get_non_existing_account(fname)
        else:
            return account

    ###############################################################

    #! TODO: discuss - would it be better to use ALPHABET?
    def test_generate_random_letter(self):
        letter = passman.generate_random_letter(alphabet)
        self.assertEqual(len(letter), 1)
        self.assertIn(letter, alphabet)

    def test_create_password(self):
        alphabet = alphabet
        length = random.randint(1, (2 * len(passman.ALPHABET)))
        password = passman.create_password(alphabet, length)
        self.assertEqual(len(password), length)
        #! TODO - should I check if letter in alphabet (for tests) rather than passman.ALPHABET?
        for letter in password:
            self.assertIn(letter, passman.ALPHABET)

    def test_check_if_account_exists_existing_acct(self):
        account = passman.Account(fname, 'bird')
        ret = account.check_if_account_exists()
        self.assertEqual(ret, True)

    def test_check_if_account_exists_non_existing_acct(self):
        account = self.get_non_existing_account(fname)
        ret = account.check_if_account_exists()
        self.assertEqual(ret, False)

    #! TODO: discuss if this is a good way to check get password guven current random pws
    #! TODO: create option to set PWs manually and change tests using manually given pws
    def test_get_password_from_file_valid_acct_default(self):
        account = passman.Account(fname, 'bird')
        with open(fname, "r") as file:
            data = csv.reader(file)
            for row in data:
                if row[0].strip() == account.acname:
                    password = row[1]
        # print_to_screen is False
        account.get_password_from_file(False)
        pw = pyperclip.paste()
        self.assertEqual(pw, password)

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
        account = passman.Account(fname, "fish")
        try:
            account.create_new_account(password_length)
            self.fail("Did not raise expected exception")
        except RuntimeError as err:
            pass
        # any unexpected exceptions will be caught by unittest framework

    def test_create_new_account_non_existing_acct(self):
        account = self.get_non_existing_account(fname)
        ret = account.check_if_account_exists()
        self.assertEqual(ret, False)
        account.create_new_account(password_length)
        ret = account.check_if_account_exists()
        self.assertEqual(ret, True)

    def test_delete_account_existing(self):
        account = self.get_non_existing_account(fname)
        account.create_new_account(password_length)
        account.delete_account()
        ret = account.check_if_account_exists()
        self.assertEqual(ret, False)

    def test_delete_account_non_existing(self):
        account = self.get_non_existing_account(fname)
        try:
            account.delete_account()
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_change_password_existing(self):
        account = self.get_non_existing_account(fname)
        account.create_new_account(alphabet, password_length)
        # print_to_screen is False
        account.get_password_from_file(False)
        pw1 = pyperclip.paste()
        account.change_password(alphabet, password_length)
        account.get_password_from_file(False)
        pw2 = pyperclip.paste()
        self.assertNotEqual(pw1, pw2)

    def test_change_password_non_existing(self):
        account = self.get_non_existing_account(fname)
        try:
            account.change_password(password_length)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_create_new_file_existing(self):
        fname = "test_file.csv"
        try:
            passman.create_new_file(fname)
            self.fail("Did not raise expected error")
        except RuntimeError as err:
            pass

    def test_create_new_file_non_existing(self):
        fname2 = self.get_non_existing_fname()
        ret = os.path.isfile(fname2)
        self.assertEqual(ret, False)
        passman.create_new_file(fname2)
        ret = os.path.isfile(fname2)
        self.assertEqual(ret, True)
        os.remove(fname2)


if __name__ == '__main__':
    unittest.main()
