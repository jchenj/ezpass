import getpass
import unittest
import pyperclip


class Tests(unittest.TestCase):

    def test_generate_random_letter(self):
        letter = getpass.generate_random_letter('abcd')
        self.assertEqual(len(letter), 1)
        self.assertIn(letter, 'abcd')

    def test_check_if_account_exists(self):
        fname = 'test-file.csv'
        account = 'bird'
        # existing account
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, True)
        # non-existing account
        account = 'zebra'
        ret = getpass.check_if_account_exists(fname, account)
        self.assertEqual(ret, False)

    def test_get_password_from_file(self):
        fname = "test-file.csv"
        account = 'bird'
        password = "feathers"
        # valid account - default
        ret = getpass.get_password_from_file(fname, account, False)
        pw = pyperclip.paste()
        self.assertEqual(pw, password)
        # CONTINUE HERE
        # not testing valid account - print screen
        # non-existingAccount = 'zebra'
        # invalid acccount - default
        # invalid acccount - print to screen







if __name__ == '__main__':
    unittest.main()