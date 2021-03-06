"""
Main file for running ezpass. For more instructions, see repo's README:
https://github.com/jchenj/ezpass
"""
import _pickle
import shlex
import argparse
import cmd
import getpass
import os
import sys
import pprint
import cryptography

#########################################
# Enable tab-completion for cmd.cmd
# https://pewpewthespells.com/blog/osx_readline.html
import readline
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
#########################################

from util import *
from pwfile import PwFile
from account import Account


# ! TODO - rename class to AcList?
# ! TODO - take acname out of class?
# ! TODO - rename acname to username?
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


class PassShell(cmd.Cmd):
    intro = 'Welcome to the ezpass interactive shell. Type "help" or "?" to ' \
            'list commands.\n'
    prompt = '(ezpass) '
    file = None

    def __init__(self, pfile):
        cmd.Cmd.__init__(self, 'tab', sys.stdin, sys.stdout)
        self.doc_header = """[n -o org] Add new account
[d -o org] Delete account
[g -o org] Get password
[ch -o org -p pass] Change password
[q] Quit
"""
        self.pfile = pfile

    # ----- basic ezpass commands -----
    # Must have pwfile before interactive mode can be used

    def run_body_handle_exceptions(self, body, parser):
        try:
            body()
        except SystemExit as error:
            # catching parse_args errors
            return
        except:
            pprint.pprint(sys.exc_info())
            parser.print_help()
            return

    def do_n(self, line):
        """[n -o org] Add a new org: NEWAC --org-name --pw-length --set-acpass"""
        parser = argparse.ArgumentParser(prog="newac")
        parser.add_argument('-o', '--org-name', type=str, help='new org '
                                                                'name',
                            required=True)
        parser.add_argument('-l', '--pw-length', type=int, required=False,
                            default=8, help='password length')
        parser.add_argument('-p', '--set-acpass', action='store_true',
                            help='set specified password', required=False)

        def body():
            args = parser.parse_args(shlex.split(line))
            if args.pw_length < 1:
                raise RuntimeError(
                    "Error. Password length must be greater than 0.")
            account = Account(self.pfile, args.org_name)
            print("Creating new account for:", args.org_name)
            acname = input("Enter username: ")
            account.create_new_account(acname, ALPHABET, args.pw_length)
            if args.set_acpass is not None:
                specified_pass = getpass.getpass(prompt="Enter password: ")
                account.set_acpass(specified_pass)
            print("Account created for:", args.org_name)

        self.run_body_handle_exceptions(body, parser)

    def do_d(self, line):
        """[d -o org] Delete account for specified org: DELAC --org-name"""
        parser = argparse.ArgumentParser(prog="delac")
        parser.add_argument('-o', '--org-name', type=str, help='org name',
                            required=True)

        def body():
            args = parser.parse_args(shlex.split(line))
            account = Account(self.pfile, args.org_name)
            account.delete_account()
            print("Deleted account for:", args.org_name)

        self.run_body_handle_exceptions(body, parser)

    def do_g(self, line):
        """[g -o org] Get password for specified org: GETACPASS --org-name --print"""
        parser = argparse.ArgumentParser(prog='getacpass')
        parser.add_argument('-o', '--org-name', type=str, help='org name',
                            required=True)
        parser.add_argument('--print', action='store_true',
                            help='print password to screen', required=False,
                            default=False)

        def body():
            args = parser.parse_args(shlex.split(line))
            account = Account(self.pfile, args.org_name)
            account.get_password_from_file(args.print)

            if args.print is False:
                print(
                    "Password for org {} in paste buffer".format(args.org_name))

        self.run_body_handle_exceptions(body, parser)

    def do_ch(self, line):
        """[ch -o org -p pass] Change password for specified org: CHACPASS --org-name set-acpass pw-length"""
        parser = argparse.ArgumentParser(prog='chacpass')
        parser.add_argument('-o', '--org-name', type=str, help='org name',
                            required=True)
        parser.add_argument('-p', '--set-acpass', action='store_true',
                            help='set specified password', required=False)
        parser.add_argument('-l', '--pw-length', type=int, required=False,
                            default=8, help='password length')

        def body():
            args = parser.parse_args(shlex.split(line))
            account = Account(self.pfile, args.org_name)
            if args.set_acpass is None:
                account.set_acpass_rand(ALPHABET, args.pw_length)
            else:
                specified_pass = getpass.getpass(prompt="Enter password: ")
                account.set_acpass(specified_pass)
            print("Password changed for account:", args.org_name)

        self.run_body_handle_exceptions(body, parser)

    def do_q(self, line):
        """[q] Quit the program"""
        print("")
        print("Goodbye!")
        sys.exit(0)


def mainfunc():
    parser = argparse.ArgumentParser(description='Password manager')
    # required
    parser.add_argument('-f', '--file', type=str, help='file name',
                        required=True)
    # choose one
    parser.add_argument('-g', '--get-acpass', type=str,
                        help='org name to get account password for')
    parser.add_argument('-no', '--new-org', type=str, help='new org name')
    parser.add_argument('-d', '--delete-account', type=str,
                        help='org to delete account for')
    parser.add_argument('-nf', '--new-file', action='store_true',
                        help='whether or not to create new file')
    parser.add_argument('-cp', '--change-acpass', type=str,
                        help='org to change password for')
    parser.add_argument('-sp', '--set-acpass', action='store_true',
                        help='whether or not to use specified password')
    # optional
    parser.add_argument('-print', '--print-to-screen', action='store_true',
                        help='print password to screen', required=False,
                        default=False)
    parser.add_argument('-l', '--password-length', type=int,
                        help='password length', required=False, default=8)
    parser.add_argument('--no-encrypt', default=False, action='store_true',
                        help='if specified, no encryption will be used')
    parser.add_argument('-a', '--alphabet', type=str, help='full alphabet',
                        required=False)
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='whether or not to use interactive mode')

    args = parser.parse_args()

    print(args)

    fname = args.file
    get_acpass_int = int(args.get_acpass is not None)
    new_org_int = int(args.new_org is not None)
    delete_account_int = int(args.delete_account is not None)
    change_acpass_int = int(args.change_acpass is not None)
    new_file_int = int(args.new_file is True)
    interactive_int = int(args.interactive is True)
    param_sum = get_acpass_int + new_org_int + delete_account_int + \
                change_acpass_int + new_file_int + interactive_int
    if param_sum > 1:
        parser.print_help()
        raise RuntimeError("Error. Can only use one of these flags at a time")
    if param_sum == 0:
        parser.print_usage()
        raise SystemExit("Error. Must use --file and "
                         "at least one additional flag")

    if args.new_file:
        # if file encrypted, new file requested & file already exists
        if os.path.isfile(fname):
            raise RuntimeError("File '{}' already exists".format(fname))
        if args.no_encrypt:
            password = None
        else:
            password = getpass.getpass(
            prompt="Enter password for file {}: ".format(fname))
        # negating no_encrypt to match semantics of 3rd param of create_new_file()
        PwFile.create_new_file(fname, password, not args.no_encrypt)
        print("New file created:", fname)
        return

    if args.no_encrypt:
        password = None
        try:
            pfile = PwFile(fname, password, not args.no_encrypt)
        except _pickle.UnpicklingError as e:
            print("Error: could not open file. Are you sure this file is not "
                  "encrypted?")
            sys.exit(1)
    else:
        while True:
            password = getpass.getpass(
                prompt="Enter password for file {}: ".format(fname))
            # Create PwFile instance based on file name & password
            # negating no_encrypt to match semantics of 3rd param of PwFile constructor
            try:
                pfile = PwFile(fname, password, not args.no_encrypt)
                break
            except cryptography.fernet.InvalidToken as e:
                print("Error: incorrect file password. Please try again")
            except UnicodeDecodeError as e:
                print("Error: Couldn't open file. Try running with "
                      "--no-encrypt")
                sys.exit(1)

    if args.interactive is True:
        shell = PassShell(pfile)
        shell.cmdloop()
        return

    if args.get_acpass is not None:
        account = Account(pfile, args.get_acpass)
        account.get_password_from_file(args.print_to_screen)
        if args.print_to_screen is False:
            print("Password for account '{}' in paste buffer".format(
                args.get_acpass))
    elif args.new_org is not None:
        if args.password_length < 1:
            raise RuntimeError("Error. Password length must be greater than 0.")
        account = Account(pfile, args.new_org)
        print("Creating new account for:", args.new_org)
        acname = input("Enter username: ")
        account.create_new_account(acname, ALPHABET, args.password_length)
        if args.set_acpass is not None:
            specified_pass = getpass.getpass(prompt="Enter password: ")
            account.set_acpass(specified_pass)
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
            specified_pass = getpass.getpass(prompt="Enter password: ")
            account.set_acpass(specified_pass)
        print("Password changed for account:", args.change_acpass)
    return


if __name__ == "__main__":
    mainfunc()
